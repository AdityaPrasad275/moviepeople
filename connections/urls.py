# connections/urls.py

from django.urls import path
from . import views

app_name = "connections"  # Namespace for URLs

urlpatterns = [
    path("send/<int:user_id>/", views.send_request, name="send_connection_request"),
    path(
        "manage/<int:connection_id>/<str:action>/",  # action will be 'accept' or 'reject'
        views.manage_request,
        name="manage_connection_request",
    ),
    path(
        "",  # Makes this the default page for the 'connections' app (e.g., /connections/)
        views.list_connections,
        name="list_connections",
    ),
    path("requests/", views.list_pending_requests, name="list_pending_requests"),
]
