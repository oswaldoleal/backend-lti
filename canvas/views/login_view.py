from pylti1p3.contrib.django import (
    DjangoOIDCLogin,
    DjangoCacheDataStorage,
)
from pylti1p3.contrib.django import DjangoDbToolConf
from rest_framework.views import APIView


class LoginView(APIView):
    def get_launch_url(self, request):
        target_link_uri = request.POST.get(
            'target_link_uri', request.GET.get('target_link_uri')
        )
        if not target_link_uri:
            raise Exception('Missing "target_link_uri" param')
        return target_link_uri

    def post(self, request, *args, **kwargs):
        tool_conf = DjangoDbToolConf()
        launch_data_storage = DjangoCacheDataStorage()
        oidc_login = DjangoOIDCLogin(
            request, tool_conf, launch_data_storage=launch_data_storage
        )
        target_link_uri = self.get_launch_url(request)
        return oidc_login.redirect(target_link_uri)
