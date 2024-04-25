from datetime import datetime
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import Event, UserEvent
from .serializers import EventSerializer, UserEventSerializer
from users.models import User


class EventListPostViewTestCase(APITestCase):
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

    def test_event_list_authenticated(self):
        Event.objects.create(title='Seminario', description='Descrição do evento 1', created_at=datetime.now(), location='Local 1')
        Event.objects.create(title='Orquestra', description='Descrição do evento 2', created_at=datetime.now(), location='Local 2')

        response = self.client.get('/events/')
        self.assertEqual(response.status_code, 200)

        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 2)

        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        self.assertEqual(response.data['results'], serializer.data)

    def test_event_list_authenticated_with_title_filter(self):
        Event.objects.create(title='Seminario', description='Descrição do evento 1', created_at=datetime.now(), location='Local 1')
        Event.objects.create(title='Orquestra', description='Descrição do evento 2', created_at=datetime.now(), location='Local 2')
        Event.objects.create(title='Workshop', description='Descrição do evento 3', created_at=datetime.now(), location='Local 3')

        response = self.client.get('/events/', {'title_contains': 'Sem'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)

        seminario_event = Event.objects.get(title='Seminario')
        serializer = EventSerializer(seminario_event)
        self.assertEqual(response.data['results'][0], serializer.data)

    def test_event_list_unauthenticated(self):
        self.client.logout()
        response = self.client.get('/events/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_event(self):
        event_data = {
            "title": "Seminario",
            "description": "Descrição do evento",
            "location": "Local do evento"
        }

        response = self.client.post('/events/', event_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(Event.objects.filter(title="Seminario").exists())

        self.assertEqual(response.data['title'], event_data['title'])
        self.assertEqual(response.data['description'], event_data['description'])
        self.assertEqual(response.data['location'], event_data['location'])

    def test_invalid_event_data(self):
        invalid_event_data = {
            "description": "Descrição do evento",
            "location": "Local do evento"
        }

        response = self.client.post('/events/', invalid_event_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class EventDetailPutViewTestCase(APITestCase):
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

        self.event = Event.objects.create(title='Seminario', description='Descrição do evento', created_at=timezone.now(), location='Local do evento')

    def test_get_event_detail(self):
        response = self.client.get(f'/events/{self.event.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = EventSerializer(self.event)
        self.assertEqual(response.data, serializer.data)

    def test_put_event(self):
        update_data = {
            "title": "Seminario Atualizado",
            "description": "Nova descrição do evento",
            "location": "Novo local do evento"
        }

        response = self.client.put(f'/events/{self.event.id}/', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.event.refresh_from_db()
        serializer = EventSerializer(self.event)
        self.assertEqual(response.data, serializer.data)

    def test_delete_event(self):
        response = self.client.delete(f'/events/{self.event.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Event.objects.filter(id=self.event.id).exists())


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

        self.event = Event.objects.create(title='Seminario', description='Descrição do evento',
                                          created_at=timezone.now(), location='Local do evento')

    def test_user_event_post(self):
        response = self.client.post(f'/events/{self.event.id}/register/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(email=self.user_data['email'])

        user_event = UserEvent.objects.filter(user=user, event=self.event).first()
        self.assertIsNotNone(user_event)

        serializer = UserEventSerializer(user_event)
        self.assertEqual(response.data, serializer.data)

    def test_user_event_post_already_registered(self):
        user = User.objects.get(email=self.user_data['email'])
        UserEvent.objects.create(user=user, event=self.event)

        response = self.client.post(f'/events/{self.event.id}/register/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'User is already registered for this event.')

    def test_user_event_delete(self):
        user = User.objects.get(email=self.user_data['email'])
        UserEvent.objects.create(user=user, event=self.event)
        response = self.client.delete(f'/events/{self.event.id}/register/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
