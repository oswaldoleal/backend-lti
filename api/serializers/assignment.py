from rest_framework import serializers

from api.models import Assignment


class AssignmentSerializer(serializers.ModelSerializer):
    gameId = serializers.IntegerField(source='game.id')

    class Meta:
        model = Assignment
        fields = ('id', 'name', 'gameId')
