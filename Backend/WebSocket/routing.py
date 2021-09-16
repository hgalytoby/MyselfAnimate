from django.urls import path

from WebSocket import consumers

websocket_urlpatterns = [
    path('', consumers.AsyncChatConsumer.as_asgi()),
]
