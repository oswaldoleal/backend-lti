from pylti1p3.contrib.django import DjangoDbToolConf, DjangoCacheDataStorage, DjangoMessageLaunch

from api.enums.role import Role
from canvas.authentication import CanvasAuth
from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from canvas.utils import PyLTISessionCache


class LaunchView(APIView):
    authentication_classes = [CanvasAuth]
    permission_classes = [IsAuthenticated]

    def get_launch_url(self, request):
        target_link_uri = request.POST.get(
            "target_link_uri", request.GET.get("target_link_uri")
        )
        if not target_link_uri:
            raise Exception('Missing "target_link_uri" param')
        return target_link_uri

    def url_params_to_str(self, params: dict):
        params_strs = []
        for key, value in params.items():
            params_strs.append(f'{key}={value}')

        return '?' + '&'.join(params_strs)

    def get_context_from_launch_data(self, launch_data):
        ld_context = launch_data['https://purl.imsglobal.org/spec/lti/claim/context']
        resource_link = launch_data['https://purl.imsglobal.org/spec/lti/claim/resource_link']
        endpoints = launch_data['https://purl.imsglobal.org/spec/lti-ags/claim/endpoint']

        context = {
            'context_id': ld_context['id'],
            'resource_id': resource_link['id'],
            'resource_name': resource_link.get('title', ''),
            'lineitem': endpoints.get('lineitem', '')
        }

        return context

    def post(self, request, *args, **kwargs):
        tool_conf = DjangoDbToolConf()
        launch_data_storage = DjangoCacheDataStorage()
        message_launch = DjangoMessageLaunch(
            request,
            tool_conf,
            launch_data_storage=launch_data_storage
        )

        PyLTISessionCache.add_request(request=request, launch_id=message_launch.get_launch_id())
        PyLTISessionCache.add_launch(launch = message_launch, launch_id=message_launch.get_launch_id())

        role = ''
        if request.user.is_student():
            role = Role.STUDENT.value
        elif request.user.is_instructor():
            role = Role.TEACHER.value

        params = {
            'user_id': request.user.lti_user_id,
            'role': role,
            'launch_id': message_launch.get_launch_id(),
            'session_id': request.COOKIES.get('lti1p3-session-id'),
        }
        params.update(self.get_context_from_launch_data(request.launch_data))

        # TODO: this URL should be a settings/env variable
        redirect_url = 'https://localhost:3000/redirect' + self.url_params_to_str(params)
        response_redirect = redirect(redirect_url)

        return response_redirect
