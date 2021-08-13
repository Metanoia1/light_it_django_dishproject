import pytest
from pytest_django.fixtures import db

from django.contrib.auth.models import User

from dishes.models import Dish, Order, Ingredient


@pytest.fixture
def i1(db):
    return Ingredient.objects.create(title="apple")


@pytest.fixture
def i2(db):
    return Ingredient.objects.create(title="orange")


@pytest.fixture
def i3(db):
    return Ingredient.objects.create(title="watermelon")


@pytest.fixture
def d1(db):
    return Dish.objects.create(title="d1_title")


@pytest.fixture
def d2(db):
    return Dish.objects.create(title="d2_title")


@pytest.fixture
def d3(db):
    return Dish.objects.create(title="r3_title")


@pytest.fixture
def d4(db):
    dish = Dish.objects.create(title="d4")
    ingredient_names = ["apple", "orange", "watermelon"]
    dish.ingredients.set(
        Ingredient.objects.create(title=name) for name in ingredient_names
    )
    return dish


@pytest.fixture
def user(db):
    return User.objects.create(
        username="username",
        password="password",
        is_staff=True,
        is_superuser=True,
    )


@pytest.fixture
def o1(user):
    dish = Dish.objects.create(title="dish_1")
    return Order.objects.create(dish=dish, user=user)


@pytest.fixture
def o2(user):
    dish = Dish.objects.create(title="dish_2")
    return Order.objects.create(dish=dish, user=user)


@pytest.fixture
def o3(user):
    dish = Dish.objects.create(title="dish_3")
    return Order.objects.create(dish=dish, user=user)
