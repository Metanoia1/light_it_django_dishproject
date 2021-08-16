from rest_framework import serializers

from dishes.models import Dish, DishIngredient
from api.validators import (
    has_numbers,
    already_exists,
    correct_amount,
    is_ingredient_exists,
)


class IngredientListSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=50, source="ingredient.title")

    class Meta:
        model = DishIngredient
        fields = ["ingredient", "title", "amount"]


class DishListSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.CharField(max_length=50, validators=[has_numbers])
    created_at = serializers.DateTimeField(format="iso-8601", read_only=True)
    ingredients = serializers.SerializerMethodField()

    def get_ingredients(self, instance):
        return IngredientListSerializer(
            instance.dishingredients, many=True, read_only=True
        ).data

    class Meta:
        model = Dish
        fields = ["url", "title", "description", "created_at", "ingredients"]


class IngredientCreateSerializer(serializers.Serializer):
    ingredient_id = serializers.IntegerField(validators=[is_ingredient_exists])
    amount = serializers.IntegerField(validators=[correct_amount])


class DishCreateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        max_length=50, validators=[has_numbers, already_exists]
    )
    created_at = serializers.DateTimeField(format="iso-8601", read_only=True)
    ingredients = IngredientCreateSerializer(many=True)

    class Meta:
        model = Dish
        fields = ["id", "title", "description", "created_at", "ingredients"]
