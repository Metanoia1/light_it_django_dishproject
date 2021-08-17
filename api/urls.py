from django.urls import path, include

from rest_framework import routers

from api import views


router = routers.DefaultRouter()
router.register(r"dishes", views.DishCRUDView)

urlpatterns = [
    path("", include(router.urls)),
    path("topdishes/", views.MostPopularDishView.as_view(), name="topdishes"),
]
