from canvas.models import LTIUser, Course
from pylti1p3.contrib.django import (
    DjangoCacheDataStorage,
    DjangoDbToolConf,
    DjangoMessageLaunch,
)
from rest_framework import authentication


class CanvasAuth(authentication.BaseAuthentication):

    def authenticate(self, request):
        tool_conf = DjangoDbToolConf()
        launch_data_storage = DjangoCacheDataStorage()
        message_launch = DjangoMessageLaunch(
            request, tool_conf, launch_data_storage=launch_data_storage
        )

        message_launch_data = message_launch.get_launch_data()
        request.launch_data = message_launch_data

        user_id = message_launch_data['sub']
        user_roles = message_launch_data['https://purl.imsglobal.org/spec/lti/claim/roles']

        email = message_launch_data.get('email', None)

        user = LTIUser.objects.filter(lti_user_id=user_id)
        if len(user) == 0:
            user = LTIUser(lti_user_id=user_id, roles=user_roles, email=email)
            LTIUser.save(user)
        else:
            user = user[0]
            user.roles = user_roles

        context = message_launch_data['https://purl.imsglobal.org/spec/lti/claim/context']
        deployment_id = message_launch_data['https://purl.imsglobal.org/spec/lti/claim/deployment_id']
        Course.objects.update_or_create(name=context['title'], id=context['id'], deployment_id=deployment_id)

        return user, None
