from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from datetime import datetime
from django.utils import timezone

from .models import Event
from .serializers import EventSerializer


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

    def test_update_event(self):
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