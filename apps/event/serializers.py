from rest_framework import serializers

from apps.event.models import Event
from apps.base.serializers import UserInfoSerializer


class EventSerializer(serializers.ModelSerializer):
    organizer = UserInfoSerializer(read_only=True)
    participators = UserInfoSerializer(many=True)

    class Meta:
        model = Event
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'created': {'read_only': True},
            'updated': {'read_only': True}
        }

    def validate(self, data):
        return data
