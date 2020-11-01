from rest_framework import serializers

from apps.base.models import User
from apps.event.models import Event
from apps.base.serializers import UserInfoSerializer


class EventSerializer(serializers.ModelSerializer):
    organizer = UserInfoSerializer(read_only=True)
    participators = UserInfoSerializer(many=True)

    class Meta:
        model = Event
        fields = [
            'id',
            'title',
            'description',
            'organizer',
            'participators',
            'notification_time',
            'start_date',
            'created',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'created': {'read_only': True},
            'updated': {'read_only': True},
        }


class EventCreateSerializer(serializers.ModelSerializer):
    organizer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    participators = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), allow_null=True)

    class Meta:
        model = Event
        fields = [
            'id',
            'title',
            'description',
            'place',
            'organizer',
            'participators',
            'notification_time',
            'start_date',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'created': {'read_only': True},
            'updated': {'read_only': True}
        }
        depth = 1

    def validate(self, data):
        organizer = data.get('organizer')
        participators = data.get('participators')
        if organizer in participators:
            raise serializers.ValidationError("Organizer cannot be a participator")
        return data
