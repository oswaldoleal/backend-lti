from api.authentication import BasicAuth
from api.serializers import UserFormSerializer
from django.contrib.auth import login
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class LoginView(generics.CreateAPIView):
    authentication_classes = [BasicAuth]
    permission_classes = [IsAuthenticated]
    serializer_class = UserFormSerializer

    def post(self, request, *args, **kwargs):
        login(request, request.user)
        return Response('ok')
