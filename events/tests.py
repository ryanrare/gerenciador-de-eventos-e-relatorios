from rest_framework.test import APIClient, APITestCase
from .models import Event
from rest_framework import status
from datetime import datetime

from .serializers import EventSerializer


class EventListPostViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        user_data = {
            "name": "testuser",
            "email": "g@g",
            "password": "g"
        }
        response = self.client.post('/users/register/', user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.login(email='g@g', password='g')

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
        response = self.client.get('/events/')

        self.assertEqual(response.status_code, 403)

    def test_create_event(self):
        event_data = {
            "title": "Seminario",
            "description": "Descrição do evento",
            "location": "Local do evento"
        }

        response = self.client.post('/events/', event_data)

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