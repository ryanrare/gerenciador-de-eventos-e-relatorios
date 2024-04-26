from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from notifications.models import UserEventNotification, User, Notification
from events.models import Event, UserEvent
from users.serializers import UserEventSerializer


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


class UserEventPostDeleteViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user_data = {
            "name": "testuser",
            "email": "g@g",
            "password": "g"
        }
        response = self.client.post('/users/register/', self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        login_data = {
            'email': 'g@g',
            'password': 'g'
        }
        response = self.client.post('/users/login/', login_data)
        self.assertEqual(response.status_code, 200)
        self.token = response.json()['jwt']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.event = Event.objects.create(
            title='Seminario', description='Descrição do evento', location='Local do evento'
        )

        self.notification = Notification.objects.create(description='Test Notification', type='update')

        self.user = User.objects.get(email=self.user_data['email'])
        self.user_event = UserEvent.objects.create(user=self.user, event=self.event)
        self.user_event_notification = UserEventNotification.objects.create(
            user_event=self.user_event, notification=self.notification, sent_by=self.user
        )

    def test_user_event_notification(self):
        response = self.client.get('/users/notifications/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user_notification(self):
        notification = UserEventNotification.objects.create(
            user_event=self.user_event, notification=self.notification, sent_by=self.user
        )

        response = self.client.delete(f'/users/notifications/{notification.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

