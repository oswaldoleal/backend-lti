from rest_framework import serializers

from api.models import QuestionBank


class QuestionBankSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionBank
        fields = ('id', 'name', 'user')
