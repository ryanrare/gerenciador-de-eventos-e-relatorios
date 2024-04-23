import json
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_user(self):
        # Dados de exemplo para o usuário
        user_data = {
            "name": "testuser",
            "email": "t@t.com",
            "password": "t"
        }

        response = self.client.post('/users/register/', user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
