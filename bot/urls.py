from django.urls import path
from .views import message_processor, send_notification_to_all

urlpatterns = [
    path('bot/read_message/', message_processor, name="read_incoming_message"),
    path('bot/notify/', send_notification_to_all, name="send_notification_to_all")
]