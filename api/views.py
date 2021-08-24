from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, mixins, generics, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from api.utils import get_most_popular_dishes
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

    def get_serializer_class(self, *args, **kwargs):
        if self.action == "create":
            return DishCreateSerializer
        return DishListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = DishModelService()
        data = service.create(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED)


class MostPopularDishView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = get_most_popular_dishes(3)
    serializer_class = DishListSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
