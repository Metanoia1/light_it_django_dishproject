import pytest


@pytest.mark.django_db
def test_get_dish_ingredients(d1, i1, i2, i3):
    assert d1.ingredients.get(title="apple") == i1
    assert d1.ingredients.get(title="cucumber") == i2
    assert d1.ingredients.get(title="watermelon") == i3
