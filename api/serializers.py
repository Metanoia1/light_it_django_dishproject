from rest_framework import serializers

from dishes.models import Dish, Ingredient
from api.validators import has_numbers


class DishSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.CharField(max_length=50, validators=[has_numbers])
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all(),
    )
    created_at = serializers.DateTimeField(format="iso-8601", read_only=True)

    class Meta:
        model = Dish
        fields = "__all__"
