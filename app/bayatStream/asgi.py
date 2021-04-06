"""
ASGI config for bayatStream project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bayatStream.settings')
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from graphene_subscriptions.consumers import GraphqlSubscriptionConsumer

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter([
        path("ws/graphql/", GraphqlSubscriptionConsumer())
    ]),
    # Just HTTP for now. (We can add other protocols later.)
})
