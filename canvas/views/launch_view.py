from rest_framework.views import APIView
from pylti1p3.contrib.django import DjangoDbToolConf
from django.http import HttpResponse, JsonResponse
from pylti1p3.contrib.django import (
    DjangoMessageLaunch,
    DjangoCacheDataStorage,
)
from pylti1p3.contrib.django import DjangoDbToolConf

from django.http.response import JsonResponse


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

        return JsonResponse(
            {
                "success": False,
                "errorMsg": "OSWALDO AYUDAME :(",
                "page_title": "PAGE_TITLE",
                "is_deep_link_launch": message_launch.is_deep_link_launch(),
                "launch_data": message_launch.get_launch_data(),
                "launch_id": message_launch.get_launch_id(),
                "curr_user_name": message_launch_data.get("name", ""),
                "curr_diff": 'si',
            }
       )
