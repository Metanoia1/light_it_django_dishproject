from django.db.models import Count
from django.core.cache import caches

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from dishes.models import Dish, Ingredient, DishIngredient


class DishModelService:
    def create(self, data):
        ingredients = [
            (get_object_or_404(Ingredient, pk=i["ingredient_id"]), i["amount"])
            for i in data["ingredients"]
        ]
        dish = Dish.objects.create(
            title=data["title"],
            description=data["description"],
        )
        DishIngredient.objects.bulk_create(
            DishIngredient(
                dish=dish,
                ingredient=ingredient[0],
                amount=ingredient[1],
            )
            for ingredient in ingredients
        )
        data = {
            "id": dish.id,
            "title": data["title"],
            "description": data["description"],
            "created_at": dish.created_at,
            "ingredients": data["ingredients"],
        }
        return Response(data, status=status.HTTP_201_CREATED)

    def get_top_dishes(self, top_number):
        return (
            Dish.objects.all()
            .annotate(orders_count=Count("orders"))
            .order_by("-orders_count")[:top_number]
        )
