from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter

from api.filters import DishDateTimeFilter
from api.services import DishModelService
from api.permissions import IsStaffUser
from api.serializers import DishListSerializer, DishCreateSerializer

from dishes.models import Dish


class DishCRUDView(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    permission_classes = [IsStaffUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ["title"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at"]
    filterset_class = DishDateTimeFilter

    def get_serializer_class(self):
        if self.action == "create":
            return DishCreateSerializer
        return DishListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class(request)
        serializer.is_valid(raise_exception=True)
        service = DishModelService()
        return service.create(serializer.data)
