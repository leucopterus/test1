from django_filters import rest_framework as filters
from rest_framework import viewsets, mixins, status, filters as rest_filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.event.models import Event
from apps.event.serializers import EventSerializer
from tools.action_based_permission import ActionBasedPermission


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsAuthenticated: ['create', 'retrieve', 'list', 'update', 'partial_update', 'destroy'],
    }
    filter_backends = [filters.DjangoFilterBackend, rest_filters.OrderingFilter]

    ordering_fields = ('created',)
    ordering = ('created',)

    def create(self, request, *args, **kwargs):
        organizer = request.user.id
        data_dict = request.data
        data_dict['organizer'] = organizer
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=data_dict)
        serializer.is_valid(raise_exception=True)
        event = self.perform_create(serializer)
        event_data = serializer_class(event).data
        headers = self.get_success_headers(event_data)
        return Response(event_data, status=status.HTTP_201_CREATED, headers=headers)
