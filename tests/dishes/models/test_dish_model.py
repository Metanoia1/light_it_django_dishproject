import pytest

from dishes.models import Dish


@pytest.mark.django_db
def test_dish_create():
    Dish.objects.create(title="new_dish")
    assert Dish.objects.count() == 1


def test_get_dish_ingredients(d4):
    milk = d4.ingredients.get(title="apple")
    orange = d4.ingredients.get(title="orange")
    watermelon = d4.ingredients.get(title="watermelon")
    assert milk.title == "apple"
    assert orange.title == "orange"
    assert watermelon.title == "watermelon"


@pytest.mark.django_db
def test_dish_str_method():
    dish = Dish.objects.create(title="salt")
    assert str(dish) == "salt"


@pytest.mark.django_db
def test_dish_ordering_by_created_at():
    dish1 = Dish.objects.create(title="salt")
    dish2 = Dish.objects.create(title="water")
    assert Dish.objects.first().pk == dish2.pk
