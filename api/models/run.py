from django.db import models

from api.models import Assignment
from canvas.models import LTIUser


class Run(models.Model):
    start_date = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    end_date = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    score = models.PositiveIntegerField()
    assignment = models.ForeignKey(
        to=Assignment,
        related_name='assignment',
        on_delete=models.CASCADE,
        help_text='Relation to corresponding assignment',
    )

    user = models.ForeignKey(
        to=LTIUser,
        related_name='user',
        on_delete=models.CASCADE,
        help_text='Relation to corresponding user',
    )
