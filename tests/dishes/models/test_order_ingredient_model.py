import pytest

from dishes.models import Ingredient, Order, OrderIngredient, Dish


@pytest.mark.django_db
def test_order_ingredient_create():
    dish = Dish.objects.create(title="new_dish")
    order = Order.objects.create(dish=dish)
    ing = Ingredient.objects.create(title="apple")
    OrderIngredient.objects.create(order=order, ingredient=ing, amount=7)
    assert OrderIngredient.objects.count() == 1
    assert OrderIngredient.objects.first().ingredient.pk == ing.pk


@pytest.mark.django_db
def test_get_ingredient():
    dish = Dish.objects.create(title="new_dish")
    order = Order.objects.create(dish=dish)
    ing = Ingredient.objects.create(title="apple")
    oi = OrderIngredient.objects.create(order=order, ingredient=ing, amount=7)
    assert oi.ingredient.pk == ing.pk


@pytest.mark.django_db
def test_get_order():
    dish = Dish.objects.create(title="new_dish")
    order = Order.objects.create(dish=dish)
    ing = Ingredient.objects.create(title="apple")
    oi = OrderIngredient.objects.create(order=order, ingredient=ing, amount=7)
    assert oi.order.pk == order.pk


@pytest.mark.django_db
def test_get_amount():
    dish = Dish.objects.create(title="new_dish")
    order = Order.objects.create(dish=dish)
    ing = Ingredient.objects.create(title="apple")
    oi = OrderIngredient.objects.create(order=order, ingredient=ing, amount=7)
    assert oi.amount == 7
