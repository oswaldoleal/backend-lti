from api.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import serializers


class UserFormSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        email = validated_data['email']
        password = make_password(validated_data['password'])
        user = User.objects.create(email=email, password=password)
        return user

    class Meta:
        model = User

        fields = [
            'id',
            'email',
            'password',
        ]

        extra_kwargs = {
            'password': {'write_only': True},
        }
