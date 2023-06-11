from datetime import timedelta, datetime, timezone

from django.http import Http404
from rest_framework import generics
from rest_framework.response import Response

from api.boards import BOARDS
from api.enums.game import Game
from api.enums.run_status import RunStatus
from api.models import GameData, Run
from api.serializers import RunSerializer, GameDataSerializer


class RunView(generics.GenericAPIView):

    def get_objects(self, assignment_id):
        try:
            return GameData.objects.filter(assignment_id=assignment_id).order_by(
                'info__order'
            )
        except GameData.DoesNotExist:
            raise Http404

    def post(self, request, *args, **kwargs):
        req = request.data

        if req['gameId'] in [Game.QUIZ.value, Game.HANGMAN.value]:
            final_data = self.get_game_data(req)
        elif req['gameId'] == Game.MEMORY.value:
            final_data = self.get_memory_game_data(req)
        elif req['gameId'] == Game.SNAKE.value:
            final_data = self.get_snake_game_data(req)

        return Response(final_data)

    def get_snake_game_data(self, req):
        start_date = datetime.now(timezone.utc)
        latest_user_run = Run.objects.filter(user_id=req['userId'],
                                             assignment_id=req['assignmentId'], state=RunStatus.IN_PROGRESS.value) \
            .order_by('id').last()

        data = GameData.objects.filter(assignment_id=req['assignmentId'])

        game_data = GameDataSerializer(data[0]).data
        board = BOARDS[game_data['info']['board']]
        answer = req.get('answer')
        user_position = req.get('userPosition')

        if latest_user_run is None:
            run = Run(
                start_date=start_date,
                end_date=start_date + timedelta(minutes=30),
                score=0, state=RunStatus.IN_PROGRESS.value, assignment_id=req['assignmentId'],
                user_id=req['userId'], user_input={"answers": {}, "position": 1, "direction": 1,
                                                   "x": 0,
                                                   "y": board['rem_per_tile'] * board['tiles_per_column'] - 2,
                                                   "rolls_left": game_data['info']['rolls_to_show_question']}
            )

            run.save()
            latest_user_run = run

        elif latest_user_run is not None:
            if answer is not None and answer['id'] != -1:
                latest_user_run.user_input['answers'][answer['id']] = answer['answerIndex']
            elif user_position is not None:
                latest_user_run.user_input['x'] = user_position['x']
                latest_user_run.user_input['y'] = user_position['y']
                latest_user_run.user_input['position'] = user_position['position']
                latest_user_run.user_input['direction'] = user_position['direction']
                latest_user_run.user_input['rolls_left'] = user_position['rollsLeft']

            latest_user_run.save()

        run = RunSerializer(latest_user_run).data

        final_data = {
            "board_data": board,
            "game_data": game_data,
            "run": run,
        }

        return final_data

    def get_memory_game_data(self, req):
        start_date = datetime.now(timezone.utc)
        latest_user_run = Run.objects.filter(user_id=req['userId'],
                                             assignment_id=req['assignmentId'], state=RunStatus.IN_PROGRESS.value) \
            .order_by('id').last()

        if latest_user_run is None:
            run = Run(
                start_date=start_date,
                end_date=start_date + timedelta(minutes=30),
                score=0, state=RunStatus.IN_PROGRESS.value, assignment_id=req['assignmentId'],
                user_id=req['userId'], user_input={'last_order': 0, "answers": {}}
            )

            run.save()
            latest_user_run = run

        run = RunSerializer(latest_user_run).data
        data = self.get_objects(req['assignmentId'])

        game_data = GameDataSerializer(data[0]).data

        final_data = {
            "game_data": game_data,
            "run": run,
            "totalCards": len(game_data['info']),
            "cards": game_data['info'],
        }

        return final_data

    def get_game_data(self, req):
        start_date = datetime.now(timezone.utc)
        latest_user_run = Run.objects.filter(user_id=req['userId'],
                                             assignment_id=req['assignmentId'], state=RunStatus.IN_PROGRESS.value)\
            .order_by('id').last()

        order = req['order']
        answers = []

        if latest_user_run is None:
            run = Run(
                start_date=start_date,
                end_date=start_date + timedelta(minutes=30),
                score=0, state=RunStatus.IN_PROGRESS.value, assignment_id=req['assignmentId'],
                user_id=req['userId'], user_input={'last_order': 0, "answers": {}}
            )

            run.save()
        else:
            run, order, answers = self.run_is_not_new(req, latest_user_run, order, answers)

        run = RunSerializer(run).data
        data = self.get_objects(req['assignmentId'])

        if len(data) == order:
            game_data = None
        else:
            game_data = GameDataSerializer(data[order]).data

        final_data = {
            "game_data": game_data,
            "run": run,
            "totalQuestions": len(data),
            "answers": answers,
        }

        return final_data

    def run_is_not_new(self, req, run, order, answers):
        latest_run_order = run.user_input.get('last_order')

        if order > latest_run_order:
            run.user_input['last_order'] = order
            if req['gameId'] == Game.QUIZ.value:
                run.user_input['answers'][order - 1] = req['answerIndex']
            elif req['gameId'] == Game.HANGMAN.value:
                run.user_input['answers'][order - 1] = req['hasWon']
            run.save()
        elif order < latest_run_order:
            order = latest_run_order
        for answer in run.user_input['answers']:
            answers.append(run.user_input['answers'][answer])

        return run, order, answers
