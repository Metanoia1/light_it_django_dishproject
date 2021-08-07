import pytest

from django.urls import reverse

from dishes.views import DishList
from dishes.models import Dish


@pytest.mark.django_db
def test_success(client):
    resp = client.get("/", follow=True)
    assert resp.status_code == 200
    assert Dish.objects.count() == 0


@pytest.mark.django_db
def test_success_rf(rf):
    request = rf.get(reverse("dishes:index"))
    resp = DishList.as_view()(request)
    assert resp.status_code == 200


@pytest.mark.django_db
def test_redirect(client):
    resp = client.get("/")
    assert resp.status_code == 302
    assert Dish.objects.count() == 0


def test_context_with_all_objects(client, d1, d2):
    resp = client.get("/", follow=True)
    assert resp.context["dishes"].count() == 2
    assert Dish.objects.count() == 2
    assert resp.status_code == 200


def test_context_with_certain_object(client, d1, d2):
    resp = client.get(f"/dishes/?title={d1.title}", follow=True)
    assert resp.context["dishes"].count() == 1
    assert resp.context["dishes"][0].title == d1.title
    assert resp.context["dishes"][0].pk == d1.pk
    assert Dish.objects.count() == 2
