from api.serializers import UserFormSerializer
from rest_framework import generics


class RegisterView(generics.CreateAPIView):
    serializer_class = UserFormSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
