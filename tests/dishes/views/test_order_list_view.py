import pytest


@pytest.mark.django_db
def test_success(client):
    resp = client.get("/dishes/orders", follow=True)
    assert resp.status_code == 200


def test_context_with_all_objects(client, o1, o2, o3, user):
    client.force_login(user)
    resp = client.get("/dishes/orders", follow=True)
    assert resp.context["orders"].count() == 3
