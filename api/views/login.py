from rest_framework.status import HTTP_400_BAD_REQUEST

from api.serializers import UserFormSerializer
from django.contrib.auth import login, authenticate
from rest_framework import generics
from rest_framework.response import Response


class LoginView(generics.CreateAPIView):
    serializer_class = UserFormSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        print(email, password)
        user = authenticate(request, username=email, password=password)
        print(user, request)
        if user is None:
            return Response(status=HTTP_400_BAD_REQUEST, data={'reason': 'user does not exist'})

        login(request, user)
        return Response('ok')
