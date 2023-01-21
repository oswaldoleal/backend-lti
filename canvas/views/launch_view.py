from django.shortcuts import redirect
from pylti1p3.contrib.django import DjangoDbToolConf
from pylti1p3.contrib.django import (
    DjangoMessageLaunch,
    DjangoCacheDataStorage,
)
from pylti1p3.contrib.django import DjangoDbToolConf
from rest_framework.views import APIView


class LaunchView(APIView):

    def get_launch_url(self, request):
        target_link_uri = request.POST.get(
            "target_link_uri", request.GET.get("target_link_uri")
        )
        if not target_link_uri:
            raise Exception('Missing "target_link_uri" param')
        return target_link_uri

    def post(self, request, *args, **kwargs):
        tool_conf = DjangoDbToolConf()
        launch_data_storage = DjangoCacheDataStorage()
        message_launch = DjangoMessageLaunch(
            request, tool_conf, launch_data_storage=launch_data_storage
        )

        message_launch_data = message_launch.get_launch_data()
        return redirect("https://localhost:3000/lti-config")
