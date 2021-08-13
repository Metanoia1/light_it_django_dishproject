import pytest

from django.contrib.auth.models import User

from dishes.models import Order, Ingredient, Dish
from dishes.utils import get_oi_initial, get_oi_formset


def test_get_dish_object(client, user, d1):
    client.force_login(user)
    resp = client.get(f"/dishes/order/{d1.id}/")
    assert resp.context["dish"].pk == d1.pk
    assert resp.status_code == 200


def test_get_dish_object_does_not_exist(client, user):
    client.force_login(user)
    resp = client.get(f"/dishes/order/1/")
    assert resp.status_code == 404


@pytest.mark.django_db
def test_formset_is_valid(client, user):
    client.force_login(user)
    dish = Dish.objects.create(title="dish")
    ingredient_names = ["apple", "orange", "watermelon"]
    dish.ingredients.set(
        Ingredient.objects.create(title=name) for name in ingredient_names
    )
    ingredients = dish.dishingredients.select_related("ingredient")
    amount = ingredients.count()
    data = {
        "form-TOTAL_FORMS": amount,
        "form-INITIAL_FORMS": "0",
        "form-MIN_NUM_FORMS": "0",
        "form-MAX_NUM_FORMS": amount,
        "form-0-ingredient": "apple",
        "form-0-amount": "7",
        "form-1-ingredient": "orange",
        "form-1-amount": "15",
        "form-2-ingredient": "watermelon",
        "form-2-amount": "5",
    }
    resp = client.post(f"/dishes/order/{dish.id}/", data=data)
    assert resp.status_code == 302
    assert Order.objects.count() == 1
    assert Order.objects.first().ingredients.count() == 3
    assert (
        list(Order.objects.first().ingredients.values_list("title", flat=True))
        == ingredient_names
    )


@pytest.mark.django_db
def test_formset_is_not_valid(client, user):
    client.force_login(user)
    dish = Dish.objects.create(title="dish")
    ingredient_names = ["apple", "orange", "watermelon"]
    dish.ingredients.set(
        Ingredient.objects.create(title=name) for name in ingredient_names
    )
    ingredients = dish.dishingredients.select_related("ingredient")
    amount = ingredients.count()
    data = {
        "form-TOTAL_FORMS": amount,
        "form-INITIAL_FORMS": "0",
        "form-MIN_NUM_FORMS": "0",
        "form-MAX_NUM_FORMS": amount,
        "form-0-ingredient": "apple",
        "form-0-amount": "7",
        "form-1-ingredient": "orange",
        "form-1-amount": "15",
        "form-2-ingredient": "watermelon",
        "form-2-amount": "xxx",
    }
    resp = client.post(f"/dishes/order/{dish.id}/", data=data)
    assert resp.status_code == 302
    assert Order.objects.count() == 0
