from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import UserSerializer, UserEventSerializer, UserNotificationSerializer
from events.models import UserEvent
from notifications.models import UserEventNotification


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()

        if user is None or not user.check_password(password):
            raise AuthenticationFailed('Unable to log in with the data provided')

        user = authenticate(request, username=email, password=password)

        refresh = RefreshToken.for_user(user)

        return JsonResponse({'jwt': str(refresh.access_token)})


class UserEventListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_events = UserEvent.objects.filter(user=user)
        serializer = UserEventSerializer(user_events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Sucess'
        }
        return response


class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserNotificationsListDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_events = UserEventNotification.objects.filter(user_event__user=user)
        serializer = UserNotificationSerializer(user_events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, notification_id):
        try:
            notification = UserEventNotification.objects.get(id=notification_id)
        except UserEventNotification.DoesNotExist:
            return Response({"error": "Notification does not exist"}, status=status.HTTP_404_NOT_FOUND)

        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
