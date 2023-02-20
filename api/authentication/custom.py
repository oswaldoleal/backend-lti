from api.models import User
from django.contrib.auth.hashers import check_password
from rest_framework import authentication


class Custom(authentication.BaseAuthentication):

    def authenticate(self, request):
        username = request.data.get('email', None)
        password = request.data.get('password', None)
        print('received:', username, password)
        try:
            user = User.objects.get(email=username)
            if check_password(password, user.password):
                return (user, None)
            return None
        except User.DoesNotExist:
            print('USER NOT FOUND')
            return None
