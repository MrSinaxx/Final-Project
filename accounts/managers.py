from typing import Any
from django.contrib.auth.models import BaseUserManager
from rest_framework.exceptions import APIException


class UnmatchedException(APIException):
    status_code = 401
    default_detail = "Not Acceptable"
    default_code = "403"


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **kwargs):
        if username is None:
            raise TypeError("User must have a username!")

        if email is None:
            raise TypeError("User must have an email!")

        if password != kwargs["confirm_password"]:
            raise UnmatchedException("Passwords doesn't match")

        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password, **kwargs):
        if password is None:
            raise TypeError("Please enter your password!")

        user = self.create_user(
            username=username, email=email, password=password, confirm_password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user
