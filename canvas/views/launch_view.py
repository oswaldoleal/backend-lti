import os
from datetime import datetime

from pylti1p3.contrib.django import DjangoDbToolConf, DjangoCacheDataStorage, DjangoMessageLaunch

from api.enums.role import Role
from api.models import Assignment
from canvas.authentication import CanvasAuth
from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from canvas.utils import PyLTISessionCache


class LaunchView(APIView):
    authentication_classes = [CanvasAuth]
    permission_classes = [IsAuthenticated]

    def get_launch_url(self, request):
        target_link_uri = request.POST.get(
            "target_link_uri", request.GET.get("target_link_uri")
        )
        if not target_link_uri:
            raise Exception('Missing "target_link_uri" param')
        return target_link_uri

    def url_params_to_str(self, params: dict):
        params_strs = []
        for key, value in params.items():
            params_strs.append(f'{key}={value}')

        return '?' + '&'.join(params_strs)

    def get_context_from_launch_data(self, launch_data):
        ld_context = launch_data['https://purl.imsglobal.org/spec/lti/claim/context']
        resource_link = launch_data['https://purl.imsglobal.org/spec/lti/claim/resource_link']
        endpoints = launch_data['https://purl.imsglobal.org/spec/lti-ags/claim/endpoint']

        context = {
            'context_id': ld_context['id'],
            'resource_id': resource_link['id'],
            'resource_name': resource_link.get('title', ''),
            'lineitem': endpoints.get('lineitem', '')
        }

        return context

    def process_time_limit(self, custom_v, params, role):
        try:
            if role == Role.STUDENT.value:
                assignment_submission_time_limit = datetime.strptime(custom_v.get('submission_time_limit'), '%Y-%m-%dT%H:%M:%S.%f%z')
                dt = datetime.now(tz=assignment_submission_time_limit.tzinfo)
                if dt >= assignment_submission_time_limit:
                    params['timeHasRunOut'] = True
        except (ValueError, TypeError):
            pass


    def process_attempts(self, request, params, role):
        assignment = Assignment.objects.filter(
            lineitem_url=request.launch_data['https://purl.imsglobal.org/spec/lti-ags/claim/endpoint']
            .get('lineitem', '')).first()

        custom_variables = request.launch_data.get('https://purl.imsglobal.org/spec/lti/claim/custom')
        if custom_variables is not None:
            params['attempts'] = custom_variables.get('assignment_attempts')
            if params['attempts'] is None:
                params['attempts'] = -1
            attempts_submitted = custom_variables.get('student_attempts')
            self.process_time_limit(custom_variables, params, role)
        elif custom_variables is None:
            params['attempts'] = -1

        if role == Role.STUDENT.value and assignment is not None:
            params['launchedAssignmentId'] = assignment.id
            params['launchedGameId'] = assignment.game_id
            if custom_variables is not None and attempts_submitted is not None and isinstance(attempts_submitted, int)\
                    and params['attempts'] <= attempts_submitted:
                params['attemptsLimitHasBeenReached'] = True

        elif assignment is not None:
            params['linkedAssignmentId'] = assignment.id
            if assignment.attempts != params['attempts'] or assignment.name != params['resource_name']:
                assignment.name = params['resource_name']
                assignment.attempts = params['attempts']
                assignment.save()



    def post(self, request, *args, **kwargs):
        tool_conf = DjangoDbToolConf()
        launch_data_storage = DjangoCacheDataStorage()
        message_launch = DjangoMessageLaunch(
            request,
            tool_conf,
            launch_data_storage=launch_data_storage
        )

        PyLTISessionCache.add_request(request=request, launch_id=message_launch.get_launch_id())
        PyLTISessionCache.add_launch(launch=message_launch, launch_id=message_launch.get_launch_id())

        role = ''
        if request.user.is_student():
            role = Role.STUDENT.value
        elif request.user.is_instructor():
            role = Role.TEACHER.value

        params = {
            'user_id': request.user.lti_user_id,
            'role': role,
            'launch_id': message_launch.get_launch_id(),
            'session_id': request.COOKIES.get('lti1p3-session-id'),
        }
        params.update(self.get_context_from_launch_data(request.launch_data))
        self.process_attempts(request, params, role)

        redirect_url = os.getenv('FRONTEND_URL') + self.url_params_to_str(params)
        response_redirect = redirect(redirect_url)

        return response_redirect
