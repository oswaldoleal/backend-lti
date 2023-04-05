from rest_framework import serializers

from api.models.game_data import GameData


class GameDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = GameData
        fields = ('assignment_id', 'info')
