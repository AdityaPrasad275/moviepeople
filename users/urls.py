from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/<str:username>/", views.profile_view, name="user_profile"),
    path("search/", views.search_users, name="search_users"),
]
