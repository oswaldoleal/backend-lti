from django.db import models


class Deployment(models.Model):

    id = models.BigIntegerField(
        primary_key=True,
        auto_created=True,
        help_text='Internal deployment ID',
    )

    lti_deployment_id = models.CharField(
        blank=False,
        null=False,
        help_text='LTI Deployment ID',
    )
