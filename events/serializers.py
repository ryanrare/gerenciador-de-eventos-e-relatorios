from rest_framework import serializers
from .models import Event, UserEvent


class UserEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEvent
        fields = ['user']


class EventSerializer(serializers.ModelSerializer):
    users_registered = serializers.SerializerMethodField()

    def get_users_registered(self, obj):
        users_registered = UserEvent.objects.filter(event=obj)
        user_serializer = UserEventSerializer(users_registered, many=True)
        return user_serializer.data

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'start_date', 'end_date', 'start_time', 'end_time',
            'created_at', 'updated_at', 'image', 'deleted_at', 'location',
            'occupancy', 'capacity', 'users_registered'
        ]