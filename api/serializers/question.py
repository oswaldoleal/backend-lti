from api.models import Question
from rest_framework import serializers


class QuestionSerializer(serializers.ModelSerializer):
    options = serializers.JSONField(source='info.options')
    question = serializers.JSONField(source='info.question')
    type = serializers.JSONField(source='info.type')

    class Meta:
        model = Question
        fields = [
            'id',
            'options',
            'question',
            'type',
        ]

class QuestionWithAnswerSerializer(serializers.ModelSerializer):
    options = serializers.JSONField(source='info.options')
    question = serializers.JSONField(source='info.question')
    type = serializers.JSONField(source='info.type')
    answer = serializers.JSONField(source='info.right_answer')
    order = serializers.JSONField(source='info.order')

    class Meta:
        model = Question
        fields = [
            'id',
            'options',
            'question',
            'type',
            'answer',
            'order'
        ]
