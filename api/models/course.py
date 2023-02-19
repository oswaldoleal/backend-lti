from .deployment import Deployment
from django.db import models


class Course(models.Model):

    id = models.BigIntegerField(
        primary_key=True,
        auto_created=True,
        help_text='LTI Course ID',
    )

    lti_resource_id = models.CharField(
        unique=True,
        blank=False,
        null=False,
        max_length=40,
        help_text='LTI resource ID from the LTI platform',
    )

    name = models.CharField(
        blank=False,
        null=False,
        help_text='LTI Course name',
    )

    register_date = models.DateTimeField(
        auto_created=True,
        help_text='Timestamp when the course first appeared in our system',
    )

    deployment = models.ForeignKey(
        to=Deployment,
        related_name='deployment',
        on_delete=models.CASCADE,
        help_text='Relation to corresponding tool deployment on an LTI Platform',
    )
