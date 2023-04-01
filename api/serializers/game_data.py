from rest_framework import serializers

from api.models.game_data import GameData


class GameDataSerializer(serializers.ModelSerializer):
    question = serializers.CharField(max_length=200)
    answers = serializers.JSONField()
    order = serializers.IntegerField()
    assignment_id = serializers.IntegerField()

    class Meta:
        model = GameData
        fields = ('question', 'answers', 'order', 'assignment_id')
