from rest_framework import serializers

from api.models.question import Question


class QuestionSerializer(serializers.ModelSerializer):
    options = serializers.JSONField(source='info.options')
    question = serializers.JSONField(source='info.question')

    class Meta:
        model = Question
        fields = ('id', 'options', 'question')
