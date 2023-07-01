from api.models import Assignment
from rest_framework import serializers


class AssignmentSerializer(serializers.ModelSerializer):
    gameId = serializers.IntegerField(source='game.id')
    requiredAssignment = serializers.IntegerField(source='required_assignment.id', required=False)

    class Meta:
        model = Assignment
        fields = [
            'id',
            'name',
            'gameId',
            'requiredAssignment',
            'attempts',
        ]
