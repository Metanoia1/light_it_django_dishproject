from rest_framework import viewsets

from api.serializers import DishSerializer

from dishes.models import Dish


class DishCrudViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
