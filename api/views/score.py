from rest_framework import generics
from rest_framework.response import Response

from api.enums.game import Game
from api.enums.run_status import RunStatus
from api.models import GameData, Run


class ScoreView(generics.GenericAPIView):
    queryset = GameData.objects

    def post(self, request):
        req = request.data
        game_data = self.queryset.filter(assignment_id=req['assignmentId']).order_by('info__order')

        if req['gameId'] in [Game.QUIZ.value, Game.HANGMAN.value]:
            return self.set_score(req, game_data)
        elif req['gameId'] == Game.MEMORY.value:
            return self.set_memory_score(req)

    def set_score(self, req, game_data):
        score = 0
        latest_user_run = Run.objects.filter(user_id=req['userId'],
                                             assignment_id=req['assignmentId'], state=RunStatus.IN_PROGRESS.value) \
            .order_by('id').last()

        for i in range(0, len(game_data)):
            answer = latest_user_run.user_input['answers'][str(i)]
            if req['gameId'] == Game.QUIZ.value and answer == game_data[i].info['right_answer']:
                score = score + 1
            elif req['gameId'] == Game.HANGMAN.value and answer:
                score = score + 1

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

    # TODO: INTEGRATE LTI SCORE
    """def postsa(self, request):
        req = request.data
        tool_conf = DjangoDbToolConf()
        launch_data_storage = DjangoCacheDataStorage()
        message_launch = ExtendedDjangoMessageLaunch.from_cache(req['launchId'], request, tool_conf, launch_data_storage=launch_data_storage)
        resource_link_id = message_launch.get_launch_data() \
            .get('https://purl.imsglobal.org/spec/lti/claim/resource_link', {}).get('id')

        if not message_launch.has_ags():
            return HttpResponseForbidden("Don't have grades!")

        sub = message_launch.get_launch_data().get('sub')
        timestamp = datetime.datetime.utcnow().isoformat() + 'Z'
        earned_score = int(req['score'])

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
            sc_line_item.set_tag('score') \
                .set_score_maximum(100) \
                .set_label('Score')
            if resource_link_id:
                sc_line_item.set_resource_id(resource_link_id)

            result = ags.put_grade(sc, sc_line_item)
        else:
            sc = Grade()
            sc.set_score_given(earned_score) \
                .set_score_maximum(100) \
                .set_timestamp(timestamp) \
                .set_activity_progress('Completed') \
                .set_grading_progress('FullyGraded') \
                .set_user_id(sub)
            result = ags.put_grade(sc)

        return JsonResponse({'success': True, 'result': result.get('body')})"""
