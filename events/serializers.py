from rest_framework import serializers
from .models import Event, UserEvent


class UserEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEvent
        fields = ['id', 'user', 'event', 'registration_date', 'is_active']


class EventSerializer(serializers.ModelSerializer):
    users_registered = serializers.SerializerMethodField()

    def get_users_registered(self, obj):
        users_registered = UserEvent.objects.filter(event=obj)
        user_serializer = UserEventSerializer(users_registered, many=True)
        return user_serializer.data

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'created_at', 'update_at', 'deleted_at', 'location', 'users_registered']
