# Signals that fires when a user logs in and logs out

from django.contrib.auth import user_logged_in, user_logged_out
from django.dispatch import receiver
from graphql_jwt.signals import token_issued
from ipware import get_client_ip

from .models import LoggedInUser
from .secure_stream_helper import ArvanStream

# @receiver(user_logged_in)
# def on_user_logged_in(sender, request, **kwargs):
#     LoggedInUser.objects.get_or_create(user=kwargs.get('user'))
#
#
# @receiver(user_logged_out)
# def on_user_logged_out(sender, **kwargs):
#     LoggedInUser.objects.filter(user=kwargs.get('user')).delete()
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


@receiver(token_issued)
def on_token_issued(sender, request, user):
    # logged_in_user, created = LoggedInUser.objects.get_or_create(user=user)
    logger.error("I am in signal")
    # if created:
    #     logged_in_user = LoggedInUser.objects.create(user=user)
    #     api = ArvanStream()
    #     client_ip, is_routable = get_client_ip(request)
    #     stream_link = api.get_secure_link(client_ip)
    #     logged_in_user.stream_link = stream_link
    #     logged_in_user.ip = client_ip
    #     logged_in_user.logged_in_before = False
    #     logged_in_user.save()
    # else:
    #     logged_in_user.stream_link = ""
    #     logged_in_user.logged_in_before = True
    #     logged_in_user.save()
