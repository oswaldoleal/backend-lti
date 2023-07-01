from canvas.models import LTIUser
from django.db import models


class QuestionBank(models.Model):

    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        to=LTIUser,
        on_delete=models.CASCADE,
        help_text='Relation to corresponding user',
    )
