from django.urls import path
from . import views

app_name = "portfolio"

urlpatterns = [
    path("", views.portfolio_list, name="portfolio_list"),
    path("create/", views.create_portfolio_item, name="create_portfolio_item"),
    path("edit/<int:pk>/", views.edit_portfolio_item, name="edit_portfolio_item"),
    path("delete/<int:pk>/", views.delete_portfolio_item, name="delete_portfolio_item"),
]
