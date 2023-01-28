from rest_framework import generics
from rest_framework.response import Response
from api.serializers import UserFormSerializer


class UserConfigView(generics.CreateAPIView):
    serializer_class = UserFormSerializer

    def post(self, request, *args, **kwargs):
        response = {
            'domain': "https://www.lti-thesis.com",
            'OIDC Redirect URL': 'https://127.0.0.1:9001/launch/',
            "OpenID Connect Initiation Url": 'http://127.0.0.1:9001/login/',
            'JWK URL': 'http://127.0.0.1:9001/jwks/',
        }
        return Response(response)
