from django.urls import path, include

from rest_framework import routers

from api import views


router = routers.DefaultRouter()
router.register(r"dishes", views.DishCrudViewSet)


urlpatterns = [
    path("", include(router.urls)),
    # я знаю, что нельзя использовать глагол
    # просто пока не придумал как сделать лучше)))
    path("createdish/", views.DishCreateView.as_view(), name="createdish"),
]
