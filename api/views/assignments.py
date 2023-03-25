from http import HTTPStatus

from rest_framework import generics
from rest_framework.response import Response

from api.models import Assignment, GameData
import json

from api.serializers import AssignmentSerializer


class AssignmentsView(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        req = request.data
        assignment = Assignment(name=req['assignmentName'], course_id=req['courseId'], game_id=req['gameId'], rounds=0)
        assignment.save()

        game_data_list = []
        for question in req['questions']:
            answers = json.dumps(question['answers'])
            game_data = GameData(question=question['question'], answers=answers, order=question['order'],
                                 right_answer=question['answer'], assignment=assignment)
            game_data_list.append(game_data)

        GameData.objects.bulk_create(game_data_list)
        return Response(HTTPStatus.OK)

    def get(self, request, *args, **kwargs):
        # user_id = request.GET.get('userId', None)
        context_id = request.GET.get('assignmentId', None)
        # user = LTIUser.objects.get(lti_user_id=user_id)
        assignments = AssignmentSerializer(Assignment.objects.filter(course_id=context_id), many=True)

        return Response({'data': assignments.data})

    def delete(self, request, *args, **kwargs):
        Assignment.objects.filter(id=request.data['id']).delete()
        return Response(HTTPStatus.OK)
