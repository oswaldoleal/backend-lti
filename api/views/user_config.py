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
        """
        This should return
        config_values = {
            'redirect_uri': 'https://backend.com/canvas/launch/',
            'title': LTI_TOOL_NAME,
            'description': LTI_TOOL_DESCRIPTION,
            'target_uri': 'https://backend.com/canvas/launch/',
            'openid_url': 'https://backend.com/canvas/login/',
            'jwk_method': {
                'public_jwk': CURRENT_DEPLOYMENT_JWK,
                'public_jwk_url': CURRENT_DEPLOYMENT_JWK_URL
            },
            'lti_advantage_services': [
                LIST_OF_OPTIONS_TO_BE_TURNED_ON
            ]
        }
        """
