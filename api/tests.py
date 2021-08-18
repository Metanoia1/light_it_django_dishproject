from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from model_bakery import baker

from dishes.models import Dish


class APIQuizTest(APITestCase):
    def setUp(self):
        super().setUp()
        self.url = "/api/dishes/"
        baker.make(Dish, _quantity=9)

    def _send_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.json()["results"]

    def test_get_list(self):
        result = self._send_get()
        self.assertEqual(9, len(result))
