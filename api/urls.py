from django.urls import path

from api import views


urlpatterns = [
    path("dishes/", views.DishListCreateView.as_view(), name="listcreate"),
    path("dishes/<int:pk>", views.DishRUDView.as_view(), name="rud"),
]
