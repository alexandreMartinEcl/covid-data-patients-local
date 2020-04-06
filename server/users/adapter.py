from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth import login

from users.auth import IDServer
from users.models import get_or_create_user


class AuthAdapter(DefaultAccountAdapter):

    def authenticate(self, request, username, password):
        try:
            tokens = IDServer.check_ids(username=username, password=password)
        except ValueError:
            return None
        user = get_or_create_user(tokens)
        return user
