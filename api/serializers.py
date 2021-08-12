from rest_framework import serializers

from dishes.models import Dish, Ingredient, DishIngredient


class DishSerializer(serializers.HyperlinkedModelSerializer):
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all(),
    )
    created_at = serializers.DateTimeField(format="iso-8601", read_only=True)

    class Meta:
        model = Dish
        fields = "__all__"


class IngredientSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    amount = serializers.IntegerField()


class DishCreationSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    created_at = serializers.DateTimeField(format="iso-8601", read_only=True)

    class Meta:
        model = Dish
        fields = "__all__"
