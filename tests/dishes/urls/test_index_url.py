import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_get_index_by_name(client):
    resp = client.get(reverse("dishes:index"))
    assert resp.status_code == 200
