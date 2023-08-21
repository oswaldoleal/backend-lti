from datetime import timedelta, datetime, timezone
from typing import Any

from django.http import Http404
from rest_framework import generics
from rest_framework.response import Response

from api.utils import BOARDS
from api.utils.enums.game import Game
from api.utils.enums.run_status import RunStatus
from api.models import GameData, Run, Question, Assignment
from api.serializers import RunSerializer, GameDataSerializer


class RunView(generics.GenericAPIView):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self.GET_GAME_DATA_METHODS = {
            Game.QUIZ: self.get_game_data,
            Game.HANGMAN: self.get_game_data,
            Game.MEMORY: self.get_memory_game_data,
            Game.SNAKE: self.get_snake_game_data,
        }

    def get_objects(self, assignment_id):
        try:
            return GameData.objects.filter(assignment_id=assignment_id).order_by(
                'info__order'
            )
        except GameData.DoesNotExist:
            raise Http404

    def get_questions(self, question_bank_id):
        try:
            return Question.objects.filter(question_bank_id=question_bank_id).order_by(
                'info__order'
            )
        except GameData.DoesNotExist:
            raise Http404

    def post(self, request, *args, **kwargs):
        game = Game(request.data['gameId'])
        return Response(self.GET_GAME_DATA_METHODS[game](request.data))

    def get_snake_game_data(self, data):
        start_date = datetime.now(timezone.utc)
        latest_user_run = Run.objects.filter(
            user_id=data['userId'],
            assignment_id=data['assignmentId'],
            state=RunStatus.IN_PROGRESS.value
        ).order_by('id').last()

        game_data = GameData.objects.filter(assignment_id=data['assignmentId'])

        game_data = GameDataSerializer(game_data[0]).data
        board = BOARDS[game_data['info']['board']]
        answer = data.get('answer')
        user_position = data.get('userPosition')

        if latest_user_run:
            if answer is not None and answer['id'] != -1:
                latest_user_run.user_input['answers'][answer['id']] = answer['answer']
            elif user_position is not None:
                latest_user_run.user_input['x'] = user_position['x']
                latest_user_run.user_input['y'] = user_position['y']
                latest_user_run.user_input['position'] = user_position['position']
                latest_user_run.user_input['direction'] = user_position['direction']
                latest_user_run.user_input['rolls_left'] = user_position['rollsLeft']
        else:
            latest_user_run = Run(
                start_date=start_date,
                end_date=start_date + timedelta(minutes=30),
                score=0,
                state=RunStatus.IN_PROGRESS.value,
                assignment_id=data['assignmentId'],
                user_id=data['userId'],
                user_input={
                    "answers": {},
                    "position": 1,
                    "direction": 1,
                    "x": 0,
                    "y": board['rem_per_tile'] * board['tiles_per_column'] - 2,
                    "rolls_left": game_data['info']['rolls_to_show_question'],
                },
            )
        latest_user_run.save()

        return_data = {
            "board_data": board,
            "game_data": game_data,
            "run": RunSerializer(latest_user_run).data,
        }
        return return_data

    def get_memory_game_data(self, data):
        start_date = datetime.now(timezone.utc)
        latest_user_run = Run.objects.filter(
            user_id=data['userId'],
            assignment_id=data['assignmentId'],
            state=RunStatus.IN_PROGRESS.value
        ).order_by('id').last()

        if latest_user_run is None:
            latest_user_run = Run(
                start_date=start_date,
                end_date=start_date + timedelta(minutes=30),
                score=0,
                state=RunStatus.IN_PROGRESS.value,
                assignment_id=data['assignmentId'],
                user_id=data['userId'],
                user_input={'last_order': 0, "answers": [], 'failed_attempts': 0}
            )
        else:
            if data['failedAttempts'] != 0:
                latest_user_run.user_input['failed_attempts'] = data['failedAttempts']
            if len(data['answers']) != 0:
                latest_user_run.user_input['answers'] = data["answers"]

        latest_user_run.save()
        game_data = GameDataSerializer(self.get_objects(data['assignmentId'])[0]).data
        final_data = {
            "game_data": game_data,
            "run": RunSerializer(latest_user_run).data,
            "totalCards": len(game_data['info']),
            "cards": game_data['info'],
        }

        return final_data

    def get_game_data(self, data):
        start_date = datetime.now(timezone.utc)
        latest_user_run = Run.objects.filter(
            user_id=data['userId'],
            assignment_id=data['assignmentId'],
            state=RunStatus.IN_PROGRESS.value
        ).order_by('id').last()

        order = data['order']
        answers = []

        if latest_user_run is None:
            user_input = {'last_order': 0, "answers": {}}

            if data['gameId'] == Game.HANGMAN.value:
                user_input['clickedLetters'] = []
            run = Run(
                start_date=start_date,
                end_date=start_date + timedelta(minutes=30),
                score=0,
                state=RunStatus.IN_PROGRESS.value,
                assignment_id=data['assignmentId'],
                user_id=data['userId'],
                user_input=user_input,
            )

        else:
            run, order, answers = self.run_is_not_new(data, latest_user_run, order, answers)

        run.save()
        run = RunSerializer(run).data

        if data['gameId'] == Game.QUIZ.value:
            assignment = Assignment.objects.get(id=data['assignmentId'])
            game_datas = self.get_questions(assignment.question_bank_id)
        elif data['gameId'] == Game.HANGMAN.value:
            game_datas = self.get_objects(data['assignmentId'])

        if len(game_datas) == order:
            game_data = None
        else:
            game_data = GameDataSerializer(game_datas[order]).data

        final_data = {
            "game_data": game_data,
            "run": run,
            "totalQuestions": len(game_datas),
            "answers": answers,
        }

        return final_data

    def run_is_not_new(self, data, run, order, answers):
        latest_run_order = run.user_input.get('last_order')

        if data['gameId'] == Game.HANGMAN.value and len(data['clickedLetters']) > len(run.user_input['clickedLetters']):
            run.user_input['clickedLetters'] = data['clickedLetters']

        if order > latest_run_order:
            run.user_input['last_order'] = order
            if data['gameId'] == Game.QUIZ.value:
                run.user_input['answers'][order - 1] = data['answerIndex']
            elif data['gameId'] == Game.HANGMAN.value:
                run.user_input['answers'][order - 1] = data['hasWon']
                run.user_input['clickedLetters'] = []

        elif order < latest_run_order:
            order = latest_run_order

        for answer in run.user_input['answers']:
            answers.append(run.user_input['answers'][answer])

        return run, order, answers
