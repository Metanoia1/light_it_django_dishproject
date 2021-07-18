from django.urls import path

from . import views


app_name = "dishes"
urlpatterns = [
    path("", views.index, name="index"),
    path("details/<int:dish_id>", views.dish_details, name="details"),
    path("orders", views.orders, name="orders"),
]
