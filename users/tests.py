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

    def setUp(self):
        self.client = APIClient()
        user_data = {
            "name": "testuser",
            "email": "g@g",
            "password": "g"
        }
        response = self.client.post('/users/register/', user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_failure(self):
        invalid_login_data = {
            "email": "rururururu",
            "password": "rararara"
        }

        response = self.client.post('/users/login/', invalid_login_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_success(self):
        login_data = {
            "email": "g@g",
            "password": "g"
        }

        response = self.client.post('/users/login/', login_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LogoutViewTestCase(APITestCase):
    def test_logout_success(self):
        response = self.client.post('/users/logout/')

        self.assertIsNone(response.cookies.get('jwt'))

