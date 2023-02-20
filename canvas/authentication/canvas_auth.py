from api.models import LTIUser
from rest_framework import authentication
from pylti1p3.contrib.django import (
    DjangoMessageLaunch,
    DjangoCacheDataStorage,
    DjangoDbToolConf,
)


class CanvasAuth(authentication.BaseAuthentication):

    def authenticate(self, request):
        tool_conf = DjangoDbToolConf()
        launch_data_storage = DjangoCacheDataStorage()
        message_launch = DjangoMessageLaunch(
            request, tool_conf, launch_data_storage=launch_data_storage
        )

        message_launch_data = message_launch.get_launch_data()

        user_id = message_launch_data['sub']
        user_roles = message_launch_data['https://purl.imsglobal.org/spec/lti/claim/roles']

        return (LTIUser(lti_user_id=user_id, roles=user_roles), None)
