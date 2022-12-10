from rest_framework import generics
from rest_framework.response import Response


class TestView(generics.RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        msg = '<h1>Test message<h1/>'
        return Response(msg)
