import json
from http import HTTPStatus

from django.http import HttpResponse
from pylti1p3.contrib.django.lti1p3_tool_config.models import LtiTool
from rest_framework import generics
from rest_framework.response import Response

from api.models import User
from backend.settings import REDIRECT_URI, TARGET_URI, OPENID_URL


class UserConfigView(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        request_json = json.loads(request.body)
        user_id = request.GET.get('userId', None)
        user = User.objects.get(id=user_id)

        tool, created = LtiTool.objects \
            .update_or_create(tool_key_id=user.ltiConfigKey_id,
                              defaults={
                                  "deployment_ids": str(request_json['deployments']).replace("'", '"'),
                                  "auth_login_url": f'{request_json["domain"]}/api/lti/authorize_redirect',
                                  "auth_token_url": f'{request_json["domain"]}/login/oauth2/token',
                                  "client_id": request_json['clientID'],
                                  "issuer": 'https://canvas.instructure.com',
                                  "key_set_url": f'{request_json["domain"]}/api/lti/security/jwks',
                                  "tool_key_id": user.ltiConfigKey_id
                              }
                              )

        if created:
            user.ltiConfig_id = tool.id
            User.save(user)

        return HttpResponse(status=HTTPStatus.OK)

    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('userId', None)
        user = User.objects.get(id=user_id)

        config_values = {
            'redirect_uri': REDIRECT_URI,
            'target_uri': TARGET_URI,
            'openid_url': OPENID_URL,
            'public_jwk': user.ltiConfigKey.public_jwk
        }

        lti_tool = LtiTool.objects.filter(tool_key_id=user.ltiConfigKey_id).first()

        if lti_tool is not None:
            tool = LtiTool.objects.get(id=lti_tool.id)
            config_values['client_id'] = tool.client_id
            config_values['domain'] = tool.auth_login_url.replace('/api/lti/authorize_redirect', '')
            config_values['deployments'] = tool.deployment_ids[2:-2].replace('"', "").split(',')


        return Response(config_values)
