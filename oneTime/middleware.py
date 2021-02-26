# Session model stores the session data
import json
import logging
import sys

from django.contrib.sessions.models import Session
from django.core import serializers
from graphql_jwt.shortcuts import get_user_by_token
from graphql_jwt.utils import get_credentials

from oneTime.models import LoggedInUser
from .secure_stream_helper import ArvanStream
from ipware import get_client_ip

logger = logging.getLogger(__name__)


class OneSessionPerUserMiddleware(object):
    done = False

    # # Called only once when the web server starts
    # def __init__(self, get_response):
    #     self.get_response = get_response
    #
    # def __call__(self, request):
    #     # Code to be executed for each request before
    #     # the view (and later middleware) are called.
    #     logger.error("I am in middleware")
    #     if request.user.is_authenticated:
    #         logged_in_user = LoggedInUser.objects.filter(user=request.user).first()
    #         if not logged_in_user:
    #             logged_in_user = LoggedInUser(user=request.user, session_key=request.session.session_key)
    #             api = ArvanStream()
    #             client_ip, is_routable = get_client_ip(request)
    #             stream_link = api.get_secure_link(client_ip)
    #             logged_in_user.stream_link = stream_link
    #             logged_in_user.ip = client_ip
    #             logged_in_user.save()
    #         stored_session_key = logged_in_user.session_key
    #         # if there is a stored_session_key  in our database and it is
    #         # different from the current session, delete the stored_session_key
    #         # session_key with from the Session table
    #
    #         api = ArvanStream()
    #         client_ip, is_routable = get_client_ip(request)
    #         stream_link = api.get_secure_link(client_ip)
    #         logged_in_user.stream_link = stream_link
    #         logged_in_user.ip = client_ip
    #         logged_in_user.session_key = request.session.session_key
    #         logged_in_user.save()
    #         if stored_session_key and stored_session_key != request.session.session_key:
    #             logged_in_user.stream_link = "No Place For Cheaters"
    #             logged_in_user.save()
    #     response = self.get_response(request)
    #
    #     # This is where you add any extra code to be executed for each request/response after
    #     # the view is called.
    #     # For this tutorial, we're not adding any code so we just return the response
    #
    #     return response
    def resolve(self, next, root, info, **args):
        if info.context and not self.done and info.field_name == "tokenAuth" and args:
            username = args["username"]
            logged_in_user, created = LoggedInUser.objects.get_or_create(user__username=username)
            if not logged_in_user.logged_in_before:
                logged_in_user.logged_in_before = True
                api = ArvanStream()
                client_ip, is_routable = get_client_ip(info.context)
                stream_link = api.get_secure_link(client_ip)
                logged_in_user.stream_link = stream_link
                logged_in_user.ip = client_ip
                logged_in_user.save()
            else:
                logged_in_user.stream_link = ""
                logged_in_user.save()
            logger.error(args["username"])
        return next(root, info, **args)

# class CheckIP:
#
#     def authenticate(self, request=None, **kwargs):
#         if request is None or getattr(request, '_jwt_token_auth', False):
#             return None
#
#         token = get_credentials(request, **kwargs)
#         client_ip, is_routable = get_client_ip(request)
#         logger.error("I am here")
#         return None
#
#     def get_user(self, user_id):
#         return None
