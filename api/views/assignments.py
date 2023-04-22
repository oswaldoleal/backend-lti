from http import HTTPStatus

from django.db import connection
from django.db.models import Case, When, Value, BooleanField, IntegerField, Sum
from rest_framework import generics
from rest_framework.response import Response

from api.enums.game import Game
from api.models import Assignment, GameData, Run
from api.serializers import AssignmentSerializer


class AssignmentsView(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        req = request.data

        if req['gameId'] in [Game.QUIZ.value, Game.HANGMAN.value, Game.MEMORY.value]:
            response = self.save_game(req)

        return response

    def save_game(self, req):
        assignment = Assignment(name=req['assignmentName'], course_id=req['courseId'], game_id=req['gameId'],
                                attempts=req['attempts'], required_assignment_id=req.get('requiredAssignmentId'))

        assignment.save()
        game_data_list = []

        if req['gameId'] in [Game.QUIZ.value, Game.HANGMAN.value]:
            for question in req['questions']:
                game_data = GameData(info=self.get_info(question, req['gameId']),
                                     assignment=assignment)
                game_data_list.append(game_data)
        elif req['gameId'] in [Game.MEMORY.value]:
            game_data = GameData(info=self.get_info(req['questions'], req['gameId']),
                                 assignment=assignment)
            game_data_list.append(game_data)

        GameData.objects.bulk_create(game_data_list)
        return Response({'data': {'id': assignment.id, 'name': assignment.name, 'gameId': assignment.game_id}})

    def get_info(self, data, game_id):
        if game_id == Game.QUIZ.value:
            return {'question': data['question'],
                    'right_answer': data['answer'],
                    'options': data['options'], 'order': data['order']}
        elif game_id == Game.HANGMAN.value:
            return {'word_to_guess': data['wordToGuess'],
                    'clue': data['clue'], 'order': data['order']}
        elif game_id == Game.MEMORY.value:
            cards = []
            for info in data:
                cards.append({'id': info['id'], 'match': info['firstMatch']})
                cards.append({'id': info['id'], 'match': info['secondMatch']})
            return {'cards': cards}

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
                if assignment_counter['assignment'] == assignment['id']:
                    if assignment_counter['in_progress']:
                        assignment['inProgress'] = True
                    assignment['attemptsLeft'] = assignment['attempts'] - assignment_counter['finished_runs']

                if assignment_counter['assignment'] == assignment.get('requiredAssignment') and assignment_counter['finished_runs'] > 0:
                    assignment['requiredAssignmentSatisfied'] = True
                    continue

    def delete(self, request, *args, **kwargs):
        Assignment.objects.filter(id=request.data['id']).delete()
        return Response(HTTPStatus.OK)

    def get_runs_by_assignment(self, ids, course_id, user_id) -> list[tuple[int, int, bool]]:
        """
        Return the list of tuples made of the assignment ids,
        if the assignment has any run in progress associated to the student, and the amount of finished runs
        """
        qs = Run.objects.filter(
            assignment__in=ids,
            user=user_id,
            assignment__course=course_id
        ).annotate(in_progress=Case(
                When(state=1,
                        then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            ),
            finished=Case(
                When(state=2,
                        then=Value(1)),
                default=Value(0),
                output_field=IntegerField()
            ),
        ).values('assignment', 'in_progress', 'finished').annotate(
            finished_runs=Sum('finished')
        )

        return qs
