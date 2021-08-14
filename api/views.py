from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import generics, mixins, status

from api.serializers import DishSerializer, DishCreationSerializer
from api.permissions import IsStaffUser
from api.filters import DishDateTimeFilter
from dishes.models import Dish, Ingredient, DishIngredient


class DishListCreateView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Dish.objects.all()
    permission_classes = [IsStaffUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ["title"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at"]
    filterset_class = DishDateTimeFilter

    def get_serializer_class(self):
        method_post = self.request.method == "POST"
        return DishSerializer if not method_post else DishCreationSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            ingredients = [
                (get_object_or_404(Ingredient, title=i["title"]), i["amount"])
                for i in serializer.data["ingredients"]
            ]
            dish = Dish.objects.create(
                title=serializer.data["title"],
                description=serializer.data["description"],
            )
            DishIngredient.objects.bulk_create(
                DishIngredient(
                    dish=dish,
                    ingredient=ingredient[0],
                    amount=ingredient[1],
                )
                for ingredient in ingredients
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
