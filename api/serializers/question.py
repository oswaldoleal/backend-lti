from api.models import Question
from rest_framework import serializers


class QuestionSerializer(serializers.ModelSerializer):
    options = serializers.JSONField(source='info.options')
    question = serializers.JSONField(source='info.question')

    class Meta:
        model = Question
        fields = [
            'id',
            'options',
            'question',
        ]
