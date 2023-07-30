from api.models import QuestionBank
from rest_framework import serializers


class QuestionBankSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionBank
        fields = [
            'id',
            'name',
            'user',
            'created_at',
            'updated_at',
        ]
