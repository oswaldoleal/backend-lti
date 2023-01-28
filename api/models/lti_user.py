from django.db import models


class LTIUser(models.Model):

    id = models.BigIntegerField(
        primary_key=True,
        auto_created=True,
        help_text='LTI User ID',
    )

    lti_user_id = models.UUIDField(
        help_text='User sub as refered by the LTI platform',
    )

    name = models.CharField(
        max_length=50,
        blank=True,
        help_text='User name in LTI platform',
    )

    email = models.EmailField(
        unique=True,
        help_text='User email in the LTI platform',
    )
