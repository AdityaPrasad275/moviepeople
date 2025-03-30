# feed/urls.py
from django.urls import path
from . import views

app_name = "feed"

urlpatterns = [
    path("create/", views.create_post, name="create_post"),
    path("", views.feed_view, name="feed_view"),  # Make feed the default for the app
    path("post/<int:post_id>/", views.post_detail, name="post_detail"),
]
