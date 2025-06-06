from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/room/(?P<room_slug>\w+)/$', consumers.RoomConsumer.as_asgi()),
    re_path(r'ws/webrtc/(?P<room_slug>\w+)/$', consumers.WebRTCConsumer.as_asgi()),
]
