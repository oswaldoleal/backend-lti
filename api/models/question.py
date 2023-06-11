from django.db import models

from api.models.question_bank import QuestionBank


class Question(models.Model):

    info = models.JSONField()
    question_bank = models.ForeignKey(
        to=QuestionBank,
        on_delete=models.CASCADE,
        help_text='Relation to corresponding bank',
    )
