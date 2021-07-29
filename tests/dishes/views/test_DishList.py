import pytest
from django.urls import reverse
from dishes.views import DishList


@pytest.mark.django_db
def test_success(client):
    resp = client.get(reverse("dishes:index"), follow=True)
    assert resp.status_code == 200


@pytest.mark.django_db
def test_success_rf(rf, settings):
    request = rf.get(reverse("dishes:index"))
    settings.LOGGING = {}
    resp = DishList.as_view()(request)
    assert resp.status_code == 200
