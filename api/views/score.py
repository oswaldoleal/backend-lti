import math

from datetime import datetime
from django.http import HttpResponseForbidden
from pylti1p3.grade import Grade
from pylti1p3.lineitem import LineItem
from rest_framework import generics
from rest_framework.response import Response

from api.utils.enums.game import Game
from api.utils.enums.run_status import RunStatus
from api.models import GameData, Run, Assignment, Question
from canvas.utils import PyLTISessionCache

from pylti1p3.contrib.django import (
    DjangoCacheDataStorage,
    DjangoDbToolConf,
    DjangoMessageLaunch,
)

class ExtendedDjangoMessageLaunch(DjangoMessageLaunch):

    def validate_nonce(self):
        """
        Probably it is bug on "https://lti-ri.imsglobal.org":
        site passes invalid "nonce" value during deep links launch.
        Because of this in case of iss == http://imsglobal.org just skip nonce validation.

        """
        iss = self.get_iss()
        deep_link_launch = self.is_deep_link_launch()
        if iss == "http://imsglobal.org" and deep_link_launch:
            return self
        return super().validate_nonce()

class ScoreView(generics.GenericAPIView):
    queryset = GameData.objects

    def post(self, request, *args, **kwargs):
        data = request.data
        assignment = Assignment.objects.get(id=data['assignmentId'])

        score = 0
        if data['gameId'] == Game.QUIZ.value:
            assignment = Assignment.objects.get(id=data['assignmentId'])
            game_data = Question.objects.filter(question_bank_id=assignment.question_bank_id).order_by('info__order')
            score = self.set_score(data, game_data)
        if data['gameId'] == Game.HANGMAN.value:
            game_data = self.queryset.filter(assignment_id=data['assignmentId']).order_by('info__order')
            score = self.set_score(data, game_data)
        if data['gameId'] == Game.MEMORY.value:
            score = self.set_memory_score(data)
        if data['gameId'] == Game.SNAKE.value:
            score = self.set_snake_score(data)

        self.set_lti_grade(request, assignment, score)
        return Response({'score': score})

    # TODO: change this functions to only calculate the scores and delegate the actual score setting 
    #       to a different function
    def set_snake_score(self, data):
        right_answers = 0
        assignment = Assignment.objects.get(id=data['assignmentId'])
        questions = Question.objects.filter(question_bank_id=assignment.question_bank_id)
        latest_user_run = Run.objects.filter(
            user_id=data['userId'],
            assignment_id=data['assignmentId'],
            state=RunStatus.IN_PROGRESS.value
        ).order_by('id').last()

        answers = latest_user_run.user_input['answers']

        # TODO: review score calculation logic
        for question in questions:
            if str(question.id) in latest_user_run.user_input['answers'] and question.info['right_answer'] == answers[str(question.id)]:
                right_answers += 1

        if len(answers) > 0:
            score = (right_answers * 100) / len(latest_user_run.user_input['answers'])
        else:
            score = 100

        latest_user_run.score = math.trunc(score)
        latest_user_run.state = RunStatus.FINISHED.value
        latest_user_run.save()

        return latest_user_run.score

    def set_score(self, data, game_data):
        right_answers = 0
        latest_user_run = Run.objects.filter(
            user_id=data['userId'],
            assignment_id=data['assignmentId'],
            state=RunStatus.IN_PROGRESS.value
        ).order_by('id').last()

        # TODO: review score calculation logic
        for i in range(len(game_data)):
            answer = latest_user_run.user_input['answers'][str(i)]
            if data['gameId'] == Game.QUIZ.value and answer == game_data[i].info['right_answer']:
                right_answers += 1
            elif data['gameId'] == Game.HANGMAN.value and answer:
                right_answers += 1

        score = (right_answers * 100) / len(game_data)
        latest_user_run.score = score
        latest_user_run.state = RunStatus.FINISHED.value
        latest_user_run.save()

        return score

    def set_memory_score(self, data):
        latest_user_run = Run.objects.filter(
            user_id=data['userId'],
            assignment_id=data['assignmentId'],
            state=RunStatus.IN_PROGRESS.value
        ).order_by('id').last()

        score = 100 - data['failedAttempts'] * data['totalMatches']

        if score > 0:
            latest_user_run.score = score
        else:
            score = 0
            latest_user_run.score = score

        latest_user_run.state = RunStatus.FINISHED.value
        latest_user_run.save()
        return score

    def set_lti_grade(self, request, assignment, score):
        # NOTE: the score should be between 0 - 100
        # TODO: abstract getting the message_launch into a separate function
        message_launch = PyLTISessionCache.get_launch(request.data['launchId'])
        
        resource_link_id = message_launch.get_launch_data().get(
            'https://purl.imsglobal.org/spec/lti/claim/resource_link',
            {}
        ).get('id')

        if not message_launch.has_ags():
            return HttpResponseForbidden("Don't have grades!")

        sub = message_launch.get_launch_data().get('sub')
        timestamp = datetime.utcnow().isoformat() + 'Z'

        ags = message_launch.get_ags()

        if ags.can_create_lineitem():
            sc = Grade()
            sc.set_score_given(score) \
                .set_score_maximum(100) \
                .set_timestamp(timestamp) \
                .set_activity_progress('Completed') \
                .set_grading_progress('FullyGraded') \
                .set_user_id(sub)

            sc_line_item = LineItem(lineitem={
                'id': assignment.lineitem_url,
                'resourceId': resource_link_id
            })
            sc_line_item.set_score_maximum(100)

            ags.put_grade(sc, sc_line_item)
