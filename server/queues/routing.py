import platform
from django.urls import re_path

from . import consumers

# if float(platform.python_version()[0:3]) > 3.6:
#     chat_room_consumer = consumers.ChatRoomConsumer.as_asgi()
# else:
#     chat_room_consumer = consumers.ChatRoomConsumer


websocket_urlpatterns = [
    re_path(r'ws/queues/(?P<room_name>\w+)/$', consumers.ChatRoomConsumer.as_asgi()),
]