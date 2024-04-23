import json
from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework import status


class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_user(self):
        user_data = {
            "name": "testuser",
            "email": "t@t.com",
            "password": "t"
        }

        response = self.client.post('/users/register/', user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginViewTestCase(APITestCase):
    def test_login_failure(self):
        invalid_login_data = {
            "email": "rururururu",
            "password": "rararara"
        }

        response = self.client.post('/users/login/', invalid_login_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
