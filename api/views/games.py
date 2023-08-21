from api.models.game import Game
from api.serializers.game import GameSerializer
from rest_framework import generics
from rest_framework.response import Response


class GamesView(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get(self, request, *args, **kwargs):
        serializer = GameSerializer(self.get_queryset().order_by('id'), many=True)
        return Response({'data': serializer.data})


class GameView(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        game = GameSerializer(Game.objects.filter(id=request.GET.get('gameId')).first())
        return Response({'data': game.data})
