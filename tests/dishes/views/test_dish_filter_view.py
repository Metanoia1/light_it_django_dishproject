from datetime import timedelta
from pytz import timezone


def test_context_with_all_objects(client, d1, d2):
    resp = client.get("/", follow=True)
    assert resp.context["dishes"].count() == 2
    assert resp.status_code == 200


def test_icontains(client, d1, d2, d3):
    resp = client.get("/dishes/filters/?title=R", follow=True)
    assert resp.context["dishes"].count() == 1
    assert resp.context["dishes"][0].pk == d3.pk
    assert resp.status_code == 200


def test_reverse_false(client, d1, d2, d3):
    resp = client.get("/dishes/filters/", follow=True)
    assert resp.context["dishes"].count() == 3
    assert resp.context["dishes"][0].pk == d3.pk
    assert resp.status_code == 200


def test_reverse_true(client, d1, d2, d3):
    resp = client.get("/dishes/filters/?reverse=on", follow=True)
    assert resp.context["dishes"].count() == 3
    assert resp.context["dishes"][0].pk == d1.pk
    assert resp.status_code == 200


def test_empty_list(client, d1, d2):
    resp = client.get("/dishes/filters/?title=d3", follow=True)
    assert resp.context["dishes"].count() == 0
    assert resp.status_code == 200


def test_gt(client, d1):
    gt = (
        timezone("Europe/Kiev")
        .localize(d1.created_at + timedelta(days=1))
        .strftime("%Y-%m-%d")
    )
    resp = client.get(f"/dishes/filters/?gt={gt}", follow=True)
    assert resp.context["dishes"].count() == 0
    assert resp.status_code == 200


def test_lt(client, d1):
    lt = (
        timezone("Europe/Kiev")
        .localize(d1.created_at - timedelta(days=1))
        .strftime("%Y-%m-%d")
    )
    resp = client.get(f"/dishes/filters/?lt={lt}", follow=True)
    assert resp.context["dishes"].count() == 0
    assert resp.status_code == 200
