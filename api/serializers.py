from rest_framework import serializers

from dishes.models import Dish, DishIngredient
from api.validators import (
    has_numbers,
    already_exists,
    correct_amount,
    is_title_exists,
)


class IngredientListSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=50, source="ingredient.title")

    class Meta:
        model = DishIngredient
        fields = ["title", "ingredient", "amount"]


class DishListSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=50, validators=[has_numbers])
    created_at = serializers.DateTimeField(format="iso-8601", read_only=True)
    ingredients = serializers.SerializerMethodField()

    def get_ingredients(self, instance):
        return IngredientListSerializer(
            instance.dishingredients, many=True, read_only=True
        ).data

    class Meta:
        model = Dish
        fields = "__all__"


class IngredientCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50, validators=[is_title_exists])
    amount = serializers.IntegerField(validators=[correct_amount])


class DishCreateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        max_length=50, validators=[has_numbers, already_exists]
    )
    ingredients = IngredientCreateSerializer(many=True)
    created_at = serializers.DateTimeField(format="iso-8601", read_only=True)

    class Meta:
        model = Dish
        fields = "__all__"
