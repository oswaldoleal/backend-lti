import json
import os
from http import HTTPStatus

from django.core.files.storage import FileSystemStorage
from django.db.models import Case, When, Value, BooleanField, IntegerField, Sum
from rest_framework import generics
from rest_framework.response import Response

from api.enums.game import Game
from api.enums.memory_type import MemoryType
from api.models import Assignment, GameData, Run
from api.serializers import AssignmentSerializer
from api.storage import ImageKitHandler


class AssignmentsView(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        req = request.data

        if req['gameId'] in [Game.QUIZ.value, Game.HANGMAN.value]:
            response = self.save_game(req)
        elif int(req['gameId']) == Game.MEMORY.value:
            response = self.save_memory_game(req, request.FILES.getlist('files'))
        elif req['gameId'] == Game.SNAKE.value:
            response = self.save_snake_game(req)

        return response

    def save_memory_game(self, req, files):
        game_id = int(req['gameId'])
        attempts = int(req['attempts'])
        questions = json.loads(req['questions'])

        if req.get('requiredAssignmentId') is not None:
            assignment_id = int(req.get('requiredAssignmentId'))
        else:
            assignment_id = None

        assignment = Assignment(name=req['assignmentName'], course_id=req['courseId'], game_id=game_id,
                                attempts=attempts, required_assignment_id=assignment_id)

        assignment.save()

        folder_path = os.environ.get('FOLDER_PATH')
        folder = f"{folder_path}/{req['courseId']}/{assignment.id}"
        os.makedirs(name=folder, exist_ok=True)
        files_names = []
        for f in files:
            files_names.append(FileSystemStorage(location=folder).save(f.name, f))

        game_data = GameData(info=self.get_info(questions, game_id, files_names, folder=folder), assignment=assignment)
        game_data.save()

        return Response({'data': {'id': assignment.id, 'name': assignment.name, 'gameId': assignment.game_id}})

    def save_snake_game(self, req):
        assignment = Assignment(name=req['assignmentName'], course_id=req['courseId'], game_id=req['gameId'],
                                attempts=req['attempts'], required_assignment_id=req.get('requiredAssignmentId'),
                                question_bank_id=req['questionBankId'])

        assignment.save()

        game_data = GameData(info=self.get_info(req, req['gameId']), assignment=assignment)
        game_data.save()

        return Response({'data': {'id': assignment.id, 'name': assignment.name, 'gameId': assignment.game_id}})

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

    def get_info(self, data, game_id, files_names=None, folder=''):
        if game_id == Game.QUIZ.value:
            return {'question': data['question'],
                    'right_answer': data['answer'],
                    'options': data['options'], 'order': data['order']}
        elif game_id == Game.HANGMAN.value:
            return {'word_to_guess': data['wordToGuess'],
                    'clue': data['clue'], 'order': data['order']}
        elif game_id == Game.MEMORY.value:
            cards = []
            files_counter = 0
            for question in data:
                cards.append({'id': question['id'], 'match': question['firstMatch'], 'type': 0})
                if question['type'] == MemoryType.TEXT.value:
                    cards.append({'id': question['id'], 'match': question['secondMatch'], 'type': 0})
                elif question['type'] == MemoryType.IMAGE.value:
                    file_name = files_names[files_counter]
                    upload_status = ImageKitHandler.upload_image(file=folder + '/' + file_name, filename=file_name)
                    cards.append({'id': question['id'], 'match': upload_status.url, 'type': 1, 'file_id': upload_status.file_id})
                    files_counter = files_counter + 1

            return {'cards': cards}
        elif game_id == Game.SNAKE.value:
            return {'board': data['board'], 'rolls_to_show_question': int(data['rollsToShowQuestion'])}

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
                print(assignment['id'], assignment_counter['assignment'])
                if assignment_counter['assignment'] == assignment['id']:
                    if assignment_counter['in_progress']:
                        assignment['inProgress'] = True
                    assignment['attemptsLeft'] = assignment['attempts'] - assignment_counter['finished_runs']
                    print(assignment['attemptsLeft'], assignment_counter)

                if assignment_counter['assignment'] == assignment.get('requiredAssignment') and assignment_counter[
                    'finished_runs'] > 0:
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
