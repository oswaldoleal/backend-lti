from http import HTTPStatus

from django.db import connection
from rest_framework import generics
from rest_framework.response import Response

from api.enums.game import Game
from api.models import Assignment, GameData
from api.serializers import AssignmentSerializer


class AssignmentsView(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        req = request.data

        if req['gameId'] in [Game.QUIZ.value, Game.HANGMAN.value]:
            response = self.save_game(req)

        return response

    def save_game(self, req):
        assignment = Assignment(name=req['assignmentName'], course_id=req['courseId'], game_id=req['gameId'],
                                attempts=req['attempts'], required_assignment_id=req.get('requiredAssignmentId'))

        assignment.save()
        game_data_list = []

        for question in req['questions']:
            game_data = GameData(info=self.get_info(question, req['gameId']),
                                 assignment=assignment)
            game_data_list.append(game_data)

        GameData.objects.bulk_create(game_data_list)
        return Response({'data': {'id': assignment.id, 'name': assignment.name, 'gameId': assignment.game_id}})

    def get_info(self, question, game_id):
        if game_id == Game.QUIZ.value:
            return {'question': question['question'],
                    'right_answer': question['answer'],
                    'options': question['options'], 'order': question['order']}
        elif game_id == Game.HANGMAN.value:
            return {'word_to_guess': question['wordToGuess'],
                    'clue': question['clue'], 'order': question['order']}

    def get(self, request, *args, **kwargs):
        context_id = request.GET.get('courseId')
        assignments = AssignmentSerializer(Assignment.objects.filter(course_id=context_id), many=True)

        if request.GET.get('isStudent') == 'True':
            assignment_counters = self.get_runs_by_assignment([assignment['id'] for assignment in assignments.data],
                                                              context_id, request.GET.get('userId'))

            self.process_student_assignments(assignments, assignment_counters)

        return Response({'data': assignments.data})


    def process_student_assignments(self, assignments, assignment_counters):
        for assignment in assignments.data:
            for assignment_counter in assignment_counters:
                if assignment_counter[0] == assignment['id']:
                    if assignment_counter[1]:
                        assignment['inProgress'] = True
                    assignment['attemptsLeft'] = assignment['attempts'] - assignment_counter[2]

                if assignment_counter[0] == assignment.get('requiredAssignment') and assignment_counter[2] > 0:
                    assignment['requiredAssignmentSatisfied'] = True
                    break

    def delete(self, request, *args, **kwargs):
        Assignment.objects.filter(id=request.data['id']).delete()
        return Response(HTTPStatus.OK)

    def get_runs_by_assignment(self, ids, course_id, user_id) -> list[tuple[int, int, bool]]:
        """
        Return the list of tuples made of the assignment ids,
        if the assignment has any run in progress associated to the student, and the amount of finished runs
        """
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT a.id, bool_or(case when ar.state = 1 then true else false end), 
            sum(case when ar.state = 2 then 1 else 0 end)
            FROM lti_app.api_assignment a join lti_app.api_run ar
            on a.id = ar.assignment_id
            WHERE a.id = ANY(%s) AND a.course_id = %s AND ar.user_id = %s::uuid 
            GROUP BY a.id""", [ids, course_id, user_id])
            return cursor.fetchall()
