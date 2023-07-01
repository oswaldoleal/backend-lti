from api.models import Game
from rest_framework import serializers


class GameSerializer(serializers.ModelSerializer):
    svgRoute = serializers.CharField(source='svg_route')

    class Meta:
        model = Game
        fields = [
            'id',
            'name',
            'description',
            'instructions',
            'svgRoute',
        ]
