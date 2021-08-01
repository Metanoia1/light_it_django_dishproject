import pytest


def test_not_found_page(client):
    resp = client.get("dishes/1", follow=True)
    assert resp.status_code == 404


def test_get_object_details(client, d1):
    resp = client.get(f"/dishes/{d1.id}", follow=True)
    assert resp.status_code == 200
    assert resp.context["dish"].pk == d1.pk
