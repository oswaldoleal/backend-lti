from api.models.game import Game
from api.models.question_bank import QuestionBank
from canvas.models import Course
from django.db import models


class Assignment(models.Model):
    name = models.CharField(
        blank=False,
        null=False,
        max_length=120,
        help_text='Course name',
    )

    register_date = models.DateTimeField(
        auto_now=True,
        help_text='Timestamp when the course first appeared in our system',
    )

    course = models.ForeignKey(
        to=Course,
        related_name='course',
        on_delete=models.CASCADE,
        help_text='Relation to corresponding course on an LTI Platform',
    )

    game = models.ForeignKey(
        to=Game,
        related_name='game',
        on_delete=models.CASCADE)

    required_assignment = models.ForeignKey('self',
                                            related_name='needed_assignment',
                                            null=True,
                                            on_delete=models.CASCADE)

    attempts = models.PositiveSmallIntegerField(
        default=3,
        help_text="Number of attempts a student has for the assignment"
    )

    question_bank = models.ForeignKey(
        to=QuestionBank,
        null=True,
        related_name='related_bank',
        on_delete=models.CASCADE,
        help_text='Relation to corresponding bank',
    )
