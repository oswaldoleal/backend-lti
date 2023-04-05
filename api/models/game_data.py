from django.db import models

from api.models import Assignment


class GameData(models.Model):

    info = models.JSONField()
    assignment = models.ForeignKey(
        to=Assignment,
        related_name='related_assignment',
        on_delete=models.CASCADE,
        help_text='Relation to corresponding assignment',
    )
