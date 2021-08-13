from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets

from api.serializers import DishSerializer
from api.permissions import IsStaffUser
from api.filters import DishDateTimeFilter
from dishes.models import Dish


class DishCrudViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [IsStaffUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ["title"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at"]
    filterset_class = DishDateTimeFilter
