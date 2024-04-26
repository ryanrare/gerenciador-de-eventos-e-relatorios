from rest_framework import serializers
from .models import User
from events.models import Event, UserEvent
from notifications.models import Notification, UserEventNotification


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'start_date', 'end_date', 'start_time', 'end_time',
            'created_at', 'updated_at', 'image', 'deleted_at', 'location', 'occupancy', 'capacity'
        ]


class UserEventSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(source='user', queryset=User.objects.all(), required=False)
    event_data = EventSerializer(source='event', read_only=True)

    class Meta:
        model = UserEvent
        fields = ['user_id', 'event_data']


class NotificationUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'description', 'type']


class UserEventNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEvent
        fields = ['id', 'event']


class UserNotificationSerializer(serializers.ModelSerializer):
    notification = NotificationUserSerializer()
    event_id = serializers.SerializerMethodField()
    event_title = serializers.SerializerMethodField()

    def get_event_id(self, obj):
        return obj.user_event.event.id if obj.user_event else None

    def get_event_title(self, obj):
        return obj.user_event.event.title if obj.user_event else None

    class Meta:
        model = UserEventNotification
        fields = ['notification', 'sent_by', 'sent_at', 'event_id', 'event_title']
