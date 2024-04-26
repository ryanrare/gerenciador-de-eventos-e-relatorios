from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import EventSerializer, UserEventSerializer
from .models import Event, UserEvent
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Q
from threading import Thread


class EventListPostView(APIView, PageNumberPagination):
    page_size = 200
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Obtém uma lista paginada de eventos.",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, description="Número da página", type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY, description="Tamanho da página",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('title_contains', openapi.IN_QUERY,
                              description="Filtra eventos por título contendo o texto especificado",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('description_contains', openapi.IN_QUERY,
                              description="Filtra eventos por descrição contendo o texto especificado",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('date', openapi.IN_QUERY, description="Filtra eventos pela data especificada",
                              type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
        ],
        responses={200: EventSerializer(many=True)}
    )
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

    @swagger_auto_schema(
        operation_description="Cria um novo evento.",
        manual_parameters=[
            openapi.Parameter('title_contains', openapi.IN_QUERY,
                              description="título contendo o texto",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('description', openapi.IN_QUERY,
                              description="descrição contendo o texto",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('start_date', openapi.IN_QUERY,
                              description="data de início no formato ano-mes-dia, que pode ser null",
                              type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
            openapi.Parameter('end_date', openapi.IN_QUERY,
                              description="data de término no formato ano-mes-dia, que pode ser null",
                              type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
            openapi.Parameter('start_time', openapi.IN_QUERY,
                              description="horário de início no formato hora:minuto, que pode ser null",
                              type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
            openapi.Parameter('end_time', openapi.IN_QUERY,
                              description="horário de término no formato hora:minuto, que pode ser null",
                              type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
            openapi.Parameter('created_at', openapi.IN_QUERY,
                              description="data de criação, que pode ser null",
                              type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
            openapi.Parameter('image', openapi.IN_QUERY,
                              description="URL da imagem, que pode ser null",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('location', openapi.IN_QUERY,
                              description="local, que pode ser null",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('occupancy', openapi.IN_QUERY,
                              description="ocupação, que pode ser null",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('capacity', openapi.IN_QUERY,
                              description="capacidade, que pode ser null",
                              type=openapi.TYPE_INTEGER),
        ],
        responses={200: EventSerializer(many=True)}
    )
    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetailPutDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Obtém detalhes de um evento.",
        manual_parameters=[
            openapi.Parameter('event_id', openapi.IN_QUERY, description="ID do evento de detalhe", type=openapi.TYPE_INTEGER),
        ],
        responses={200: EventSerializer(many=True)}
    )
    def get(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Atualiza um evento já criado. No off cria uma notificação onde vc pode acessar em outro endpoit,"
                              " alem de mandar para todos conectados no socket que o evento foi atualizado",
        manual_parameters=[
            openapi.Parameter('title_contains', openapi.IN_QUERY,
                              description="título contendo o texto",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('description', openapi.IN_QUERY,
                              description="descrição contendo o texto",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('start_date', openapi.IN_QUERY,
                              description="data de início no formato ano-mes-dia, que pode ser null",
                              type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
            openapi.Parameter('end_date', openapi.IN_QUERY,
                              description="data de término no formato ano-mes-dia, que pode ser null",
                              type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
            openapi.Parameter('start_time', openapi.IN_QUERY,
                              description="horário de início no formato hora:minuto, que pode ser null",
                              type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
            openapi.Parameter('end_time', openapi.IN_QUERY,
                              description="horário de término no formato hora:minuto, que pode ser null",
                              type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
            openapi.Parameter('created_at', openapi.IN_QUERY,
                              description="data de criação, que pode ser null",
                              type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
            openapi.Parameter('image', openapi.IN_QUERY,
                              description="URL da imagem, que pode ser null",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('location', openapi.IN_QUERY,
                              description="local, que pode ser null",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('occupancy', openapi.IN_QUERY,
                              description="ocupação, que pode ser null",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('capacity', openapi.IN_QUERY,
                              description="capacidade, que pode ser null",
                              type=openapi.TYPE_INTEGER),
        ],
        responses={200: EventSerializer(many=True)}
    )
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

    @swagger_auto_schema(
        operation_description="Cancela um evento com base no id da query.",
        responses={
            204: "O evento foi cancelado com sucesso.",
            404: "O evento não foi encontrado."
        }
    )
    def delete(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        event.delete()
        return Response(
            {"detail": f"the {event_id} event you are registered for has been canceled"},
            status=status.HTTP_204_NO_CONTENT
        )


class UserEventPostView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Registra o usuário logado para um evento.",
        manual_parameters=[
            openapi.Parameter('event_id', openapi.IN_PATH, description="ID do evento", type=openapi.TYPE_INTEGER)
        ],
        responses={
            201: "Usuário registrado com sucesso para o evento.",
            400: "O usuário já está registrado para este evento."
        }
    )
    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        user = request.user

        if UserEvent.objects.filter(user=user, event=event).exists():
            return Response({'error': 'User is already registered for this event.'}, status=status.HTTP_400_BAD_REQUEST)

        user_event = UserEvent.objects.create(user=user, event=event)
        serializer = UserEventSerializer(user_event)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Remove o registro de um usuário para um evento.",
        manual_parameters=[
            openapi.Parameter('event_id', openapi.IN_PATH, description="ID do evento", type=openapi.TYPE_INTEGER)
        ],
        responses={
            204: "Registro do usuário removido com sucesso para o evento.",
            400: "O usuário não está registrado para este evento."
        }
    )
    def delete(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        user = request.user

        try:
            user_event = get_object_or_404(UserEvent, user=user, event=event)
            user_event.delete()
            return Response({"detail": "RegisterEventUser deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except UserEvent.DoesNotExist:
            return Response({'error': 'User is not registered for this event.'}, status=status.HTTP_400_BAD_REQUEST)
