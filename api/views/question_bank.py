from http import HTTPStatus

from django.http import HttpResponse
from rest_framework import generics
from rest_framework.response import Response

from api.models import QuestionBank, Question
from api.serializers import QuestionBankSerializer


class QuestionBankView(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        question_bank = QuestionBankSerializer(QuestionBank.objects.filter(user=request.GET.get('userId')), many=True)
        return Response({'data': question_bank.data})

    def post(self, request, *args, **kwargs) -> HttpResponse:
        try:
            if request.data.get('id') is None:
                question_bank = QuestionBank(name=request.data['bankName'], user_id=request.data['userId'])
            else:
                question_bank = QuestionBank.objects.get(id=request.data.get('id'))
                question_bank.name = request.data['bankName']
                Question.objects.filter(question_bank_id=request.data.get('id')).delete()

            question_bank.save()

            questions = []
            for question in request.data['questions']:
                game_data = Question(info=self.get_info(question), question_bank_id=question_bank.id)
                questions.append(game_data)

            Question.objects.bulk_create(questions)
            return HttpResponse(status=HTTPStatus.OK)
        except Exception as e:
            print(e)
            return HttpResponse(status=HTTPStatus.INTERNAL_SERVER_ERROR)

    def get_info(self, data):
        return {
            'question': data['question'],
            'right_answer': data['answer'],
            'options': data['options'],
            'order': data['order'],
            'type': data['type']}

    def delete(self, request, *args, **kwargs):
        QuestionBank.objects.filter(id=request.data['id']).delete()
        return Response(HTTPStatus.OK)
