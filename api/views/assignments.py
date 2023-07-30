import json
import os

from django.core.files.storage import FileSystemStorage
from django.db.models import Case, When, Value, BooleanField, IntegerField, Sum
from http import HTTPStatus
from rest_framework import generics
from rest_framework.response import Response
from typing import Any

from api.models import Assignment, GameData, Run
from api.serializers import AssignmentSerializer
from api.utils.enums import Game
from api.utils.enums import MemoryType
from api.utils.storage import ImageKitHandler


class AssignmentsView(generics.GenericAPIView):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self.SAVE_GAME_METHODS = {
            Game.QUIZ: self.save_quiz_game,
            Game.HANGMAN: self.save_hangman_game,
            Game.MEMORY: self.save_memory_game,
            Game.SNAKE: self.save_snake_game,
        }

    # HTTP METHODS
    def get(self, request, *args, **kwargs):
        context_id = request.GET.get('courseId')
        assignments = AssignmentSerializer(Assignment.objects.filter(course_id=context_id), many=True)

        if request.GET.get('isStudent') == 'true':
            assignment_counters = self.get_runs_by_assignment([assignment['id'] for assignment in assignments.data],
                                                              context_id, request.GET.get('userId'))

            self.process_student_assignments(assignments, assignment_counters)

        return Response({'data': assignments.data})

    def post(self, request, *args, **kwargs):
        game = Game(int(request.data['gameId']))
        return self.SAVE_GAME_METHODS[game](request)

    def delete(self, request, *args, **kwargs):
        Assignment.objects.filter(id=request.data['id']).delete()
        return Response(HTTPStatus.OK)

    # LOGIC METHODS
    def save_memory_game(self, request):
        data = request.data
        game_id = int(data['gameId'])
        attempts = int(data['attempts'])
        questions = json.loads(data['questions'])
        files = request.FILES.getlist('files')

        assignment_id = int(data.get('requiredAssignmentId')) if data.get('requiredAssignmentId') else None

        assignment = Assignment(
            name=data['assignmentName'],
            course_id=data['courseId'],
            game_id=game_id,
            attempts=attempts,
            required_assignment_id=assignment_id,
        )
        assignment.save()

        # TODO: turn this into a util function
        folder_path = os.environ.get('FOLDER_PATH')
        folder = f"{folder_path}/{data['courseId']}/{assignment.id}"
        os.makedirs(name=folder, exist_ok=True)
        files_names = []
        for f in files:
            files_names.append(FileSystemStorage(location=folder).save(f.name, f))

        game_data = GameData(info=self.get_game_info(questions, game_id, files_names, folder=folder), assignment=assignment)
        game_data.save()

        return Response({'data': {'id': assignment.id, 'name': assignment.name, 'gameId': assignment.game_id}})

    def save_snake_game(self, request):
        data = request.data
        assignment = Assignment(name=data['assignmentName'], course_id=data['courseId'], game_id=data['gameId'],
                                attempts=data['attempts'], required_assignment_id=data.get('requiredAssignmentId'),
                                question_bank_id=data['questionBankId'])
        assignment.save()

        game_data = GameData(info=self.get_game_info(data, data['gameId']), assignment=assignment)
        game_data.save()

        return Response({
            'data': {
                'id': assignment.id,
                'name': assignment.name,
                'gameId': assignment.game_id,
            },
        })

    def save_quiz_game(self, request):
        data = request.data
        assignment = Assignment(name=data['assignmentName'], course_id=data['courseId'], game_id=data['gameId'],
                                attempts=data['attempts'], required_assignment_id=data.get('requiredAssignmentId'),
                                question_bank_id=data['questionBankId'])
        assignment.save()

        return Response({
            'data': {
                'id': assignment.id,
                'name': assignment.name,
                'gameId': assignment.game_id,
            },
        })

    def save_hangman_game(self, request):
        data = request.data
        assignment = Assignment(
            name=data['assignmentName'],
            course_id=data['courseId'],
            game_id=data['gameId'],
            attempts=data['attempts'],
            required_assignment_id=data.get('requiredAssignmentId'),
        )

        assignment.save()
        game_data_list = []

        for question in data['questions']:
            game_data = GameData(info=self.get_game_info(question, data['gameId']), assignment=assignment)
            game_data_list.append(game_data)

        GameData.objects.bulk_create(game_data_list)
        return Response({'data': {'id': assignment.id, 'name': assignment.name, 'gameId': assignment.game_id}})

    def get_game_info(self, data, game_id, files_names=None, folder=''):
        if game_id == Game.QUIZ.value:
            return {
                'question': data['question'],
                'right_answer': data['answer'],
                'options': data['options'],
                'order': data['order'],
                'type': data['type']
            }

        if game_id == Game.HANGMAN.value:
            return {
                'word_to_guess': data['wordToGuess'],
                'clue': data['clue'],
                'order': data['order'],
            }

        if game_id == Game.MEMORY.value:
            cards = []
            files_counter = 0
            for question in data:
                cards.append({
                    'id': question['id'],
                    'match': question['firstMatch'],
                    'type': 0,
                })

                if question['type'] == MemoryType.TEXT.value:
                    cards.append({
                        'id': question['id'],
                        'match': question['secondMatch'],
                        'type': 0,
                    })
                elif question['type'] == MemoryType.IMAGE.value:
                    file_name = files_names[files_counter]
                    upload_status = ImageKitHandler.upload_image(file=folder + '/' + file_name, filename=file_name)
                    cards.append({
                        'id': question['id'],
                        'match': upload_status.url,
                        'type': 1,
                        'file_id': upload_status.file_id,
                    })
                    files_counter = files_counter + 1

            return {'cards': cards}

        if game_id == Game.SNAKE.value:
            return {
                'board': data['board'],
                'rolls_to_show_question': int(data['rollsToShowQuestion']),
            }

    def process_student_assignments(self, assignments, assignment_counters):
        for assignment in assignments.data:
            for assignment_counter in assignment_counters:
                if assignment_counter['assignment'] == assignment['id']:
                    if assignment_counter['in_progress']:
                        assignment['inProgress'] = True
                    assignment['attemptsLeft'] = assignment['attempts'] - assignment_counter['finished_runs']

                if assignment_counter['assignment'] == assignment.get('requiredAssignment') and assignment_counter[
                    'finished_runs'] > 0:
                    assignment['requiredAssignmentSatisfied'] = True
                    continue

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
