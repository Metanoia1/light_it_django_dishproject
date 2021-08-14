from django.urls import path

from api import views


urlpatterns = [
    path("dishes/", views.DishListCreateView.as_view(), name="list_create"),
]
