from django.urls import re_path
from chat import consumers

# Main Websocket URLS HUB
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<chatroom>\w+)/$', consumers.ChatRoomConsumer.as_asgi()),
]