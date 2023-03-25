from api.models.game import Game
from api.serializers.game import GameSerializer
from rest_framework import generics
from rest_framework.response import Response


class GamesView(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get(self, request, *args, **kwargs):
        serializer = GameSerializer(self.get_queryset(), many=True)
        return Response({'data': serializer.data})
