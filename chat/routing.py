from django.urls import re_path
from django.urls.conf import path
from . import consumers

websocket_urlpatterns = [
    # re_path(r'ws/chat/(?P<chatroom>\w+)/$', consumers.ChatRoomConsumer.as_asgi()),
    re_path(r'ws/connect_to_server/>\w+)/$', consumers.ChatRoomConsumer.as_asgi()),
    # path('ws/connect_to_server')
]