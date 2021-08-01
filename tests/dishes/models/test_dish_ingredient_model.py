import pytest

from dishes.models import Ingredient, DishIngredient, Dish


@pytest.mark.django_db
def test_dish_ingredient_create():
    dish = Dish.objects.create(title="new_dish")
    ing = Ingredient.objects.create(title="apple")
    DishIngredient.objects.create(dish=dish, ingredient=ing, amount=7)
    assert DishIngredient.objects.count() == 1
    assert DishIngredient.objects.first().ingredient.pk == ing.pk


@pytest.mark.django_db
def test_get_ingredient():
    dish = Dish.objects.create(title="new_dish")
    ing = Ingredient.objects.create(title="apple")
    di = DishIngredient.objects.create(dish=dish, ingredient=ing, amount=7)
    assert di.ingredient.pk == ing.pk


@pytest.mark.django_db
def test_get_dish():
    dish = Dish.objects.create(title="new_dish")
    ing = Ingredient.objects.create(title="apple")
    di = DishIngredient.objects.create(dish=dish, ingredient=ing, amount=7)
    assert di.dish.pk == dish.pk


@pytest.mark.django_db
def test_get_amount():
    dish = Dish.objects.create(title="new_dish")
    ing = Ingredient.objects.create(title="apple")
    di = DishIngredient.objects.create(dish=dish, ingredient=ing, amount=7)
    assert di.amount == 7
