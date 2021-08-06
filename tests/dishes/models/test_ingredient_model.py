import pytest

from dishes.models import Ingredient


@pytest.mark.django_db
def test_ingredient_str_method():
    apple = Ingredient.objects.create(title="apple")
    assert str(apple) == "apple"
