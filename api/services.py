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
        return {
            "id": dish.id,
            "title": data["title"],
            "description": data["description"],
            "created_at": dish.created_at,
            "ingredients": data["ingredients"],
        }
