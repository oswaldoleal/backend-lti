from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from pylti1p3.contrib.django.lti1p3_tool_config.models import LtiTool


class User(AbstractBaseUser):

    email = models.EmailField(
        unique=True,
        help_text='User email',
    )

    ltiConfig = models.ForeignKey(
        to=LtiTool,
        on_delete=models.CASCADE,
        related_name='ltiConfig',
        help_text='Relation to corresponding tool deployment on an LTI Platform',
        null=True
    )
