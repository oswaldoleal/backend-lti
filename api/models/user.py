from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from pylti1p3.contrib.django.lti1p3_tool_config.models import LtiToolKey


class User(AbstractBaseUser):

    email = models.EmailField(
        unique=True,
        help_text='User email',
    )

    ltiConfigKey = models.ForeignKey(
        to=LtiToolKey,
        on_delete=models.CASCADE,
        related_name='ltiConfigKey',
        help_text='Relation to corresponding tool deployment on an LTI Platform',
        null=True
    )
