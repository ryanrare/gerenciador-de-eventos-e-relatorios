from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .serializers import EventSerializer
from .models import Event
from django.utils import timezone
from django.shortcuts import get_object_or_404


class EventListPostView(APIView, PageNumberPagination):
    page_size = 200
    permission_classes = [IsAuthenticated]

    def get(self, request):
        page_number = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size', 20)

        paginator = PageNumberPagination()
        paginator.page_size = page_size
        paginator.page = page_number

        events = Event.objects.all()
        results_page = paginator.paginate_queryset(events, request)
        serializer = EventSerializer(results_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetailPutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.validated_data['update_at'] = timezone.now().date()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        event.delete()
        return Response({"detail": "Event deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
