from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'created_at', 'update_at', 'deleted_at', 'location']
