from api.models import QuestionBank
from django.db import models


class Question(models.Model):

    info = models.JSONField()
    question_bank = models.ForeignKey(
        to=QuestionBank,
        on_delete=models.CASCADE,
        help_text='Relation to corresponding bank',
    )
