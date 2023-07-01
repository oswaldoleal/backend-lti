from rest_framework import generics
from rest_framework.response import Response

from api.models import QuestionBank
from api.serializers import QuestionBankSerializer


class QuestionBankView(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        questionBank = QuestionBankSerializer(QuestionBank.objects.filter(user=request.GET.get('userId')), many=True)
        return Response({'data': questionBank.data})
