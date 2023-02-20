from typing import Any, Optional
from django.contrib.auth.backends import BaseBackend
from django.http import HttpRequest
from django.contrib.auth.models import AbstractBaseUser, User
from rest_framework import authentication


class CanvasAuth(authentication.BaseAuthentication):

    def authenticate(self, request):
        print(request.body)
        return (User(), None)
