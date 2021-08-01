import pytest

from dishes.models import Order, Dish


@pytest.mark.django_db
def test_order_create():
    dish = Dish.objects.create(title="new_dish")
    Order.objects.create(dish=dish)
    assert Order.objects.count() == 1


@pytest.mark.django_db
def test_get_order_dish():
    dish = Dish.objects.create(title="salmon")
    order = Order.objects.create(dish=dish)
    dish = order.dish
    assert dish.title == "salmon"


@pytest.mark.django_db
def test_order_ordering_by_id():
    dish = Dish.objects.create(title="pizza")
    order1 = Order.objects.create(dish=dish)
    order2 = Order.objects.create(dish=dish)
    assert Order.objects.first().pk == order2.pk
