import pytest

from django.urls import reverse


def test_get_order_by_name(client, d1):
    resp = client.get(reverse("dishes:order", args=[d1.pk]))
    assert resp.status_code == 200
