from api.models import User
from django.contrib.auth.hashers import check_password
from rest_framework import authentication


class BasicAuth(authentication.BaseAuthentication):

    def authenticate(self, request):
        username = request.data.get('email', None)
        password = request.data.get('password', None)
        
        try:
            user = User.objects.get(email=username)
            if check_password(password, user.password):
                return user, None
            return None
        except User.DoesNotExist:
            return None
