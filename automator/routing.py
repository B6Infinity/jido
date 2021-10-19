from enum import auto
from django.urls import re_path
from django.urls.conf import path
import chat.consumers
import automator.consumers

# Main Websocket URLS HUB
websocket_urlpatterns = [
    re_path(r'ws/connect_to_server/$', automator.consumers.ConnectToServer.as_asgi()),
]