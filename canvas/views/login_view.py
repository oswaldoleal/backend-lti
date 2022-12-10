from rest_framework import generics
from rest_framework.response import Response


class LoginView(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        msg = '<h1>Test message<h1/>'
        return Response(msg)
