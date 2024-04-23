from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.status import HTTP_201_CREATED
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from .serializers import EventSerializer
from .models import Event


class EventListPostView(APIView, PageNumberPagination):
    page_size = 200

    @method_decorator(login_required())
    def get(self, request):
        events = Event.objects.all()
        events = self.paginate_queryset(events, self.request)
        events_serializer = EventSerializer(events, many=True).data
        return self.get_paginated_response(events_serializer)

    def post(self, request):
        pass


class EventDetailPutView(APIView):

    def get(self, request, event_id):
        pass

    def put(self, request, event_id):
        pass

    def delete(self, request, event_id):
        pass