# messaging/urls.py
from django.urls import path
from . import views

app_name = "messaging"  # Optional: Namespacing for clarity

urlpatterns = [
    # URL for processing the message sending form submission
    path("send/", views.send_message, name="send_message"),
    # URL pattern for viewing a conversation with a specific user
    path("<str:username>/", views.conversation_view, name="conversation"),
]
