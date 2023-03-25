from rest_framework import serializers

from api.models.game import Game


class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = '__all__'
