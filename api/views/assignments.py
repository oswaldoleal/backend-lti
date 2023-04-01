from http import HTTPStatus

from rest_framework import generics
from rest_framework.response import Response

from api.enums.run_status import RunStatus
from api.models import Assignment, GameData, Run
from api.serializers import AssignmentSerializer


class AssignmentsView(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        req = request.data
        assignment = Assignment(name=req['assignmentName'], course_id=req['courseId'], game_id=req['gameId'],
                                attempts=req['attempts'])

        assignment.save()

        game_data_list = []
        for question in req['questions']:
            game_data = GameData(question=question['question'], answers=question['answers'], order=question['order'],
                                 right_answer=question['answer'], assignment=assignment)
            game_data_list.append(game_data)

        GameData.objects.bulk_create(game_data_list)
        return Response({'data': {'id': assignment.id, 'name': assignment.name, 'gameId': assignment.game_id}})

    def get(self, request, *args, **kwargs):
        context_id = request.GET.get('assignmentId', None)
        assignments = AssignmentSerializer(Assignment.objects.filter(course_id=context_id), many=True)

        for assignment in assignments.data:
            run_query_set = Run.objects.filter(assignment_id=assignment['id'], user_id=request.GET.get('userId'),
                                               state=RunStatus.IN_PROGRESS.value)
            if run_query_set.exists():
                assignment['inProgress'] = True

        return Response({'data': assignments.data})

    def delete(self, request, *args, **kwargs):
        Assignment.objects.filter(id=request.data['id']).delete()
        return Response(HTTPStatus.OK)
