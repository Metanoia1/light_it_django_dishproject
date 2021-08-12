from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializers import DishSerializer, DishCreationSerializer

from dishes.models import Dish, DishIngredient, Ingredient


class DishCrudViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class DishCreateView(generics.GenericAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishCreationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
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
