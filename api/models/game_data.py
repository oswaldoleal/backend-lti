from django.db import models

from api.models import Assignment


class GameData(models.Model):

    question = models.TextField()
    answers = models.JSONField()
    order = models.PositiveIntegerField()
    right_answer = models.PositiveIntegerField()
    assignment = models.ForeignKey(
        to=Assignment,
        related_name='related_assignment',
        on_delete=models.CASCADE,
        help_text='Relation to corresponding assignment',
    )
