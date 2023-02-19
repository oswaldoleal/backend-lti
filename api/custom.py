from django.contrib.auth.backends import BaseBackend
from api.models import User
from django.contrib.auth.hashers import check_password


class Custom(BaseBackend):

    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if check_password(password, user.password):
                return user
            return None
        except User.DoesNotExist:
            return None
