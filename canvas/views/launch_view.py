from pylti1p3.contrib.django import DjangoDbToolConf, DjangoCacheDataStorage, DjangoMessageLaunch

from canvas.authentication import CanvasAuth
from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


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
        context = {
            'context_id': ld_context['id'],
            'context_type': ld_context['type'][0].split('/')[-1],
        }

        return context

    def post(self, request, *args, **kwargs):
        # TODO: pass the role and context to the frontend
        tool_conf = DjangoDbToolConf()
        launch_data_storage = DjangoCacheDataStorage()
        message_launch = DjangoMessageLaunch(request, tool_conf,
                                             launch_data_storage=launch_data_storage)
        params = {
            'user_id': request.user.lti_user_id,
            'is_student': request.user.is_student(),
            'is_instructor': request.user.is_instructor(),
            'launch_id': message_launch.get_launch_id()
        }
        params.update(self.get_context_from_launch_data(request.launch_data))

        redirect_url = 'https://localhost:3000/redirect' + self.url_params_to_str(params)
        return redirect(redirect_url)
