import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_get_filters_by_name(client):
    resp = client.get(reverse("dishes:filters"))
    assert resp.status_code == 200
