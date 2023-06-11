import random

from rest_framework import generics
from rest_framework.response import Response

from api.enums.game import Game
from api.enums.run_status import RunStatus
from api.models import Question, Run, Assignment
from api.serializers import QuestionSerializer


class QuestionsView(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        req = request.data

        if req['gameId'] in [Game.QUIZ.value]:
            response = self.save_game(req)
        elif req['gameId'] == Game.SNAKE.value:
            response = self.save_snake_game(req)

        return response

    def save_snake_game(self, req):
        assignment = Assignment.objects.filter(id=req['assignmentId'])
        questions = Question.objects.filter(question_bank_id=assignment[0].question_bank_id)
        latest_user_run = Run.objects.filter(user_id=req['userId'],
                                             assignment_id=req['assignmentId'], state=RunStatus.IN_PROGRESS.value) \
            .order_by('id').last()

        unused_questions = []

        for obj in questions:
            if str(f"{obj.id}") not in getattr(latest_user_run, 'user_input')['answers']:
                unused_questions.append(obj)
            else:
                pass
                # key_already_exists
        unused_question = unused_questions[random.randint(0, len(unused_questions) - 1)]
        return Response(QuestionSerializer(unused_question).data)
