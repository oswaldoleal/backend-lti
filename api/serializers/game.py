from rest_framework import serializers

from api.models.game import Game


class GameSerializer(serializers.ModelSerializer):
    svgRoute = serializers.CharField(source='svg_route')

    class Meta:
        model = Game
        fields = ('id', 'name', 'description', 'instructions', 'svgRoute')
