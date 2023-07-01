from api.models import Assignment
from canvas.models import LTIUser
from django.db import models


class Run(models.Model):
    start_date = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    end_date = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    user_input = models.JSONField(default=dict)
    score = models.PositiveIntegerField()
    state = models.PositiveSmallIntegerField()
    assignment = models.ForeignKey(
        to=Assignment,
        related_name='assignment',
        on_delete=models.CASCADE,
        help_text='Relation to corresponding assignment',
    )

    user = models.ForeignKey(
        to=LTIUser,
        related_name='user',
        to_field='lti_user_id',
        on_delete=models.CASCADE,
        help_text='Relation to corresponding user',
    )
