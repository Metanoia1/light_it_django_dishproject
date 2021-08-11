from rest_framework import serializers

from dishes.models import Dish, Ingredient


class DishSerializer(serializers.HyperlinkedModelSerializer):
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all(),
    )
    created_at = serializers.DateTimeField(format="iso-8601", read_only=True)

    class Meta:
        model = Dish
        fields = "__all__"
