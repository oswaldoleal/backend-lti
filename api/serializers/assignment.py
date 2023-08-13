from api.models import Assignment
from rest_framework import serializers


class AssignmentSerializer(serializers.ModelSerializer):
    gameId = serializers.IntegerField(source='game.id')
    registerDate = serializers.DateTimeField(source='register_date')
    requiredAssignment = serializers.IntegerField(source='required_assignment.id', required=False)
    questionBank = serializers.IntegerField(source='question_bank.id', required=False)

    class Meta:
        model = Assignment
        fields = [
            'id',
            'name',
            'gameId',
            'requiredAssignment',
            'attempts',
            'registerDate',
            'questionBank'
        ]
