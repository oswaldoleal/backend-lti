from api.models import GameData
from rest_framework import serializers


class GameDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = GameData
        fields = [
            'id',
            'assignment_id',
            'info',
        ]
