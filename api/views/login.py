from api.serializers import UserFormSerializer
from django.contrib.auth import login, authenticate
from rest_framework import generics
from rest_framework.response import Response


class LoginView(generics.CreateAPIView):
    serializer_class = UserFormSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        print(user, request)
        login(request, user)

        return Response('ok')
