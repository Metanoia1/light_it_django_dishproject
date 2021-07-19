from django.urls import path

from . import views


app_name = "dishes"

urlpatterns = [
    path("", views.DishList.as_view(), name="index"),
    path("details/<int:pk>", views.DishDetail.as_view(), name="details"),
    path("orders", views.OrderList.as_view(), name="orders"),
    path("create-order/<int:dish_id>", views.create_order, name="order"),
]
