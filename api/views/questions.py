import random
from http import HTTPStatus

from django.http import HttpResponse
from rest_framework import generics
from rest_framework.response import Response

from api.utils.enums.run_status import RunStatus
from api.models import Question, Run, Assignment
from api.serializers import QuestionSerializer, QuestionWithAnswerSerializer


class QuestionsView(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        questions = QuestionWithAnswerSerializer(Question.objects.filter(
            question_bank_id=request.GET.get('bankId')),
            many=True)
        return Response({'data': questions.data})

    def post(self, request, *args, **kwargs):
        return self.get_random_question(request.data)

    def get_random_question(self, data):
        assignment = Assignment.objects.filter(id=data['assignmentId'])
        questions = Question.objects.filter(question_bank_id=assignment[0].question_bank_id)
        latest_user_run = Run.objects.filter(
            user_id=data['userId'],
            assignment_id=data['assignmentId'],
            state=RunStatus.IN_PROGRESS.value
        ).order_by('id').last()

        unused_questions = []

        for obj in questions:
            if str(obj.id) not in getattr(latest_user_run, 'user_input')['answers']:
                unused_questions.append(obj)

        if len(unused_questions) > 0:
            unused_question = unused_questions[random.randint(0, len(unused_questions) - 1)]
            return Response(QuestionSerializer(unused_question).data)
        else:
            return Response({'code': HTTPStatus.NO_CONTENT})
