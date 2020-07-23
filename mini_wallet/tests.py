from django.test import TestCase

# Create your tests here.
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APITestCase
from django.test import Client
from rest_framework.reverse import reverse_lazy

from mini_wallet.models import WalletUser


class TestInitializeAccountViewSet(APITestCase):
    def test_user_create(self):
        """
        test create user
        """
        data = {'customer_xid': 'ea0212d3-abd6-406f-8c67-868e814a2436'}
        url = reverse_lazy("init-list")
        response = self.client.post(url, data=data, format="json", follow=True)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def setUp(self):
        self.client = Client()