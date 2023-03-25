from django.db import models


class Course(models.Model):

    id = models.CharField(
        primary_key=True,
        auto_created=True,
        help_text='LTI Course ID',
    )

    name = models.CharField(
        blank=False,
        null=False,
        max_length=120,
        help_text='LTI Course name',
    )

    register_date = models.DateTimeField(
        auto_now=True,
        help_text='Timestamp when the course first appeared in our system',
    )

    deployment_id = models.CharField(
        help_text='Relation to corresponding deployment on an LTI Platform',
    )
