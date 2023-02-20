from django.shortcuts import redirect
from pylti1p3.contrib.django import (
    DjangoMessageLaunch,
    DjangoCacheDataStorage,
    DjangoDbToolConf,
)
from rest_framework.views import APIView

from canvas.authentication import CanvasAuth
from rest_framework.permissions import IsAuthenticated


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

    def post(self, request, *args, **kwargs):
        # TODO: pass the role and context to the frontend
        return redirect("https://localhost:3000/lti-config")
