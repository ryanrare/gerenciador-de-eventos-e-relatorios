from rest_framework import serializers
from .models import User
from events.models import Event, UserEvent


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
        fields = ['id', 'title', 'description', 'date', 'created_at', 'update_at', 'deleted_at', 'location']


class UserEventSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(source='user', queryset=User.objects.all(), required=False)
    event_data = EventSerializer(source='event', read_only=True)

    class Meta:
        model = UserEvent
        fields = ['user_id', 'event_data']