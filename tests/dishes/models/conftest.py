import pytest
from pytest_django.fixtures import db

from dishes.models import *


@pytest.fixture
def i1(db):
    return Ingredient.objects.create(title="apple")


@pytest.fixture
def i2(db):
    return Ingredient.objects.create(title="cucumber")


@pytest.fixture
def i3(db):
    return Ingredient.objects.create(title="watermelon")


@pytest.fixture
def d1(db, i1, i2, i3):
    ingredients = [i1, i2, i3]
    dish = Dish.objects.create(title="d1")
    dish_ingredients = [
        DishIngredient(dish=dish, ingredient=i) for i in ingredients
    ]
    DishIngredient.objects.bulk_create(dish_ingredients)
    return dish
