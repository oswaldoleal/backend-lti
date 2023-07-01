from django.db import models
from canvas.models import LTIUser


class AvatarConfig(models.Model):

    config = models.JSONField()

    user = models.ForeignKey(
        to=LTIUser,
        on_delete=models.CASCADE,
        related_name='ltiUser',
        help_text='Relation to lti user',
    )
