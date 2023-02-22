import json

from pylti1p3.contrib.django.lti1p3_tool_config.models import LtiTool
from rest_framework import generics
from rest_framework.response import Response

from api.models import User
from api.serializers import UserFormSerializer
from backend.settings import REDIRECT_URI, TARGET_URI, OPENID_URL, PUBLIC_JWK


class UserConfigView(generics.GenericAPIView):
    serializer_class = UserFormSerializer

    def post(self, request, *args, **kwargs):
        """TODO: THIS SHOULD UPDATE FIELDS IN THE DATABASE"""
        """TODO: FIX AND CLEAN THIS ABOMINATION"""
        request_json = json.loads(request.body)

        created_tool = LtiTool.objects.update_or_create(client_id=request_json['clientID'],
                                                        auth_login_url=request_json['authLoginURL'],
                                                        auth_token_url=request_json['authTokenURL'],
                                                        deployment_ids=request_json['deployments'],
                                                        issuer=request_json['oidcIssuer'],
                                                        key_set_url=request_json['publicKeyURL'],
                                                        tool_key_id=1
                                                        )

        user_id = request.GET.get('userId', None)
        user = User.objects.get(id=user_id)
        user.ltiConfig_id = created_tool.id
        User.save(user)

        return Response("success")

    def get(self, request, *args, **kwargs):
        """TODO: FIX AND CLEAN THIS ABOMINATION"""
        user_id = request.GET.get('userId', None)
        user = User.objects.get(id=user_id)

        config_values = {
            'redirect_uri': REDIRECT_URI,
            'target_uri': TARGET_URI,
            'openid_url': OPENID_URL,
            'public_jwk': PUBLIC_JWK
        }

        if user.ltiConfig_id is not None:
            """TODO: THE USER WON'T HAVE A LINKED LTI TOOL WHEN STARTING"""
            tool = LtiTool.objects.get(id=user.ltiConfig_id)
            config_values['client_id'] = tool.client_id
            config_values['oidc_issuer'] = tool.issuer
            config_values['auth_login_url'] = tool.auth_login_url
            config_values['public_key_url'] = tool.key_set_url
            config_values['auth_token_url'] = tool.auth_token_url
            config_values['deployments'] = tool.deployment_ids


        return Response(config_values)
        """
        This should return
        config_values = {
            'title': LTI_TOOL_NAME,
            'description': LTI_TOOL_DESCRIPTION,
            'jwk_method': {
                'public_jwk': CURRENT_DEPLOYMENT_JWK,
                'public_jwk_url': CURRENT_DEPLOYMENT_JWK_URL
            },
            'lti_advantage_services': [
                LIST_OF_OPTIONS_TO_BE_TURNED_ON
            ]
        }
        """
