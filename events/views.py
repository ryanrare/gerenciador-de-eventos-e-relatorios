from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
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

    @method_decorator(login_required())
    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetailPutView(APIView):

    @method_decorator(login_required())
    def get(self, request, event_id):
        pass

    @method_decorator(login_required())
    def put(self, request, event_id):
        pass

    @method_decorator(login_required())
    def delete(self, request, event_id):
        pass