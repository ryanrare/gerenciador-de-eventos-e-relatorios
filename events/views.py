from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import EventSerializer, UserEventSerializer
from .models import Event, UserEvent
from notifications.models import Notification, UserEventNotification
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Q
from threading import Thread


class EventListPostView(APIView, PageNumberPagination):
    page_size = 200
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def get(self, request):
        page_number = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size', self.page_size)
        query_params_mapping = {
            'title_contains': 'title__icontains',
            'description_contains': 'description__icontains',
            'date': 'date',
            'created_at': 'created_at',
            'capacity': 'capacity',
            'occupancy': 'occupancy',
        }

        query = Q()
        for param, field_lookup in query_params_mapping.items():
            value = request.query_params.get(param)
            if value:
                query |= Q(**{field_lookup: value})

        events = Event.objects.filter(query)

        paginator = PageNumberPagination()
        paginator.page_size = page_size
        paginator.page = page_number

        results_page = paginator.paginate_queryset(events, request)
        serializer = EventSerializer(results_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetailPutDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        serializer = EventSerializer(event, data=request.data)

        if serializer.is_valid():
            serializer.validated_data['updated_at'] = timezone.now().date()
            event = serializer.save()

            from notifications.utils import send_notifications_to_users

            def send_notifications(title, type_notification, event, user):
                send_notifications_to_users(
                    title=event.title,
                    type_notification=type_notification,
                    event=event,
                    user=user
                )

            notification_event = Thread(
                target=send_notifications,
                args=(event.title, "update", event, request.user,)
            )
            notification_event.start()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        event.delete()
        return Response(
            {"detail": f"the {event_id} event you are registered for has been canceled"},
            status=status.HTTP_204_NO_CONTENT
        )


class UserEventPostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        user = request.user

        if UserEvent.objects.filter(user=user, event=event).exists():
            return Response({'error': 'User is already registered for this event.'}, status=status.HTTP_400_BAD_REQUEST)

        user_event = UserEvent.objects.create(user=user, event=event)
        serializer = UserEventSerializer(user_event)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        user = request.user

        try:
            user_event = get_object_or_404(UserEvent, user=user, event=event)
            user_event.delete()
            return Response({"detail": "RegisterEventUser deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except UserEvent.DoesNotExist:
            return Response({'error': 'User is not registered for this event.'}, status=status.HTTP_400_BAD_REQUEST)
