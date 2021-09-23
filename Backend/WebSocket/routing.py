from django.urls import path

from WebSocket import consumers

websocket_urlpatterns = [
    path('ws/', consumers.AsyncChatConsumer.as_asgi()),
]
