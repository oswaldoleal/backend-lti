import math
from datetime import datetime

from django.http import HttpResponseForbidden
from pylti1p3.contrib.django import DjangoDbToolConf, DjangoCacheDataStorage, DjangoMessageLaunch
from pylti1p3.grade import Grade
from pylti1p3.lineitem import LineItem
from rest_framework import generics
from rest_framework.response import Response

from api.enums.game import Game
from api.enums.run_status import RunStatus
from api.models import GameData, Run, Assignment, Question
from canvas.views.requests_cache import RequestCache

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

    def post(self, request):
        print(request.COOKIES, request.headers)
        request.COOKIES['lti1p3-session-id'] = request.data['sessionId']
        print(request.COOKIES, request.headers)

        # tool_conf = DjangoDbToolConf()
        # launch_data_storage = DjangoCacheDataStorage()
        # message_launch = DjangoMessageLaunch(
        #     request, tool_conf, launch_data_storage=launch_data_storage
        # )
        # ags = message_launch.get_ags()
        # print(ags)
        message_launch = DjangoMessageLaunch.from_cache()


        req = request.data

        if req['gameId'] in [Game.QUIZ.value, Game.HANGMAN.value]:
            game_data = self.queryset.filter(assignment_id=req['assignmentId']).order_by('info__order')
            return self.set_score(req, game_data)
        elif req['gameId'] == Game.MEMORY.value:
            return self.set_memory_score(req)
        elif req['gameId'] == Game.SNAKE.value:
            return self.set_snake_score(req)

        #self.set_lti_grade(request)

    def set_snake_score(self, req):
        right_answers = 0
        assignment = Assignment.objects.get(id=req['assignmentId'])
        questions = Question.objects.filter(question_bank_id=assignment.question_bank_id)
        latest_user_run = Run.objects.filter(user_id=req['userId'],
                                             assignment_id=req['assignmentId'], state=RunStatus.IN_PROGRESS.value) \
            .order_by('id').last()

        answers = latest_user_run.user_input['answers']

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

        return Response({'score': latest_user_run.score})

    def set_score(self, req, game_data):
        right_answers = 0
        latest_user_run = Run.objects.filter(user_id=req['userId'],
                                             assignment_id=req['assignmentId'], state=RunStatus.IN_PROGRESS.value) \
            .order_by('id').last()

        for i in range(0, len(game_data)):
            answer = latest_user_run.user_input['answers'][str(i)]
            if req['gameId'] == Game.QUIZ.value and answer == game_data[i].info['right_answer']:
                right_answers = right_answers + 1
            elif req['gameId'] == Game.HANGMAN.value and answer:
                right_answers = right_answers + 1

        score = (right_answers * 100) / len(game_data)
        latest_user_run.score = score
        latest_user_run.state = RunStatus.FINISHED.value
        latest_user_run.save()

        return Response({'score': score})

    def set_memory_score(self, req):
        latest_user_run = Run.objects.filter(user_id=req['userId'],
                                             assignment_id=req['assignmentId'], state=RunStatus.IN_PROGRESS.value) \
            .order_by('id').last()

        score = 100 - req['failedAttempts'] * req['totalMatches']

        latest_user_run.score = score
        latest_user_run.state = RunStatus.FINISHED.value
        latest_user_run.save()

        return Response({'score': score})

    #REALLY BASIC VERSION
    def set_lti_grade(self, request):
        req = request.data
        tool_conf = DjangoDbToolConf()
        launch_data_storage = DjangoCacheDataStorage()
        good_request = RequestCache.get_request(req['launchId'])
        message_launch = ExtendedDjangoMessageLaunch.from_cache(req['launchId'], good_request, tool_conf,
                                                                launch_data_storage=launch_data_storage)

        """message_launch = DjangoMessageLaunch(request, tool_conf,
                                             launch_data_storage=launch_data_storage)"""
        resource_link_id = message_launch.get_launch_data() \
            .get('https://purl.imsglobal.org/spec/lti/claim/resource_link', {}).get('id')

        i = 1
        if not message_launch.has_ags():
            return HttpResponseForbidden("Don't have grades!")

        sub = message_launch.get_launch_data().get('sub')
        timestamp = datetime.utcnow().isoformat() + 'Z'
        earned_score = int(3000)

        ags = message_launch.get_ags()

        if ags.can_create_lineitem():
            sc = Grade()
            sc.set_score_given(earned_score) \
                .set_score_maximum(100) \
                .set_timestamp(timestamp) \
                .set_activity_progress('Completed') \
                .set_grading_progress('FullyGraded') \
                .set_user_id(sub)

            sc_line_item = LineItem()
            sc_line_item.set_tag('BASIC LTI') \
                .set_score_maximum(100) \
                .set_label('BASIC LTI')
            if resource_link_id:
                sc_line_item.set_resource_id(resource_link_id)

            ags.put_grade(sc, sc_line_item)

        #return JsonResponse({'success': True, 'result': result.get('body')})
