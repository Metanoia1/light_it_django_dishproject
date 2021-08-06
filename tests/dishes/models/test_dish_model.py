import pytest

from dishes.models import Dish


@pytest.mark.django_db
def test_dish_str_method():
    dish = Dish.objects.create(title="salt")
    assert str(dish) == "salt"
