# tickets/routing.py
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/api/tickets", consumers.TicketConsumer.as_asgi()),  # Certifique-se de que o caminho está correto
]
