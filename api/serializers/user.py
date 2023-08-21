import string
import random

from pylti1p3.contrib.django.lti1p3_tool_config.models import LtiToolKey, LtiTool

from api.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from api.utils.crypto import KeyGenerator


class UserFormSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        email = validated_data['email']
        password = make_password(validated_data['password'])

        private_key, public_key = KeyGenerator.generate_keys()
        lti_tool_key = LtiToolKey(name=''.join(random.choices(string.ascii_lowercase, k=10)),
                                  public_key=public_key.decode(), private_key=private_key.decode())
        lti_tool_key.save()
        user = User.objects.create(email=email, password=password, ltiConfigKey_id=lti_tool_key.id)
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
