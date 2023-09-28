from django.http import Http404, HttpResponse
from http import HTTPStatus
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from canvas.models import AvatarConfig, LTIUser
from canvas.serializers import AvatarSerializer


class AvatarView(generics.GenericAPIView):

    def get(self, request):
        try:
            avatar_config = get_object_or_404(AvatarConfig, user_id=request.GET.get('userId'))
            return Response({'data': AvatarSerializer(avatar_config).data})
        except Http404:
            return Response({'data': None})

    def post(self, request, *args, **kwargs):
        try:
            user = get_object_or_404(LTIUser, lti_user_id=request.data['userId'])
        except Http404:
            return HttpResponse(status=HTTPStatus.BAD_REQUEST, reason="userId does not belong to any user")

        AvatarConfig.objects.update_or_create(user_id=user.pk,
                                              defaults={'user_id': user.pk,
                                                        'config': request.data['config']}
                                              )
        return Response({'status': HTTPStatus.OK})
