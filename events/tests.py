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

    def test_event_list_authenticated(self):
        self.client.login(email='g@g', password='g')

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
