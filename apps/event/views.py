from django.db.models import Q
from django_filters import rest_framework as filters
from rest_framework import viewsets, status, filters as rest_filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.base.custom_permissions import IsOrganizerOrParticapatorOrAdmin
from apps.event.models import Event
from apps.event.serializers import EventSerializer, EventCreateSerializer
from tools.action_based_permission import ActionBasedPermission
from tools.email_notification import send_mail_notification


class EventViewSet(viewsets.ModelViewSet):
    http_method_names = ['post', 'head', 'get', 'patch', 'put', 'delete']
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    input_serializer_class = EventCreateSerializer
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsAuthenticated: ['create', 'list'],
        IsOrganizerOrParticapatorOrAdmin: ['retrieve', 'update', 'partial_update', 'destroy'],
    }
    filter_backends = [filters.DjangoFilterBackend, rest_filters.OrderingFilter]

    ordering_fields = ('created',)
    ordering = ('created',)

    EMAIL_SUBJECT = 'New Task Created'

    def list(self, request, *args, **kwargs):
        user_id = request.user.id
        if not request.user.is_superuser:
            queryset = self.get_queryset().prefetch_related().filter(
                Q(organizer_id=user_id) | Q(participators__id__in=[user_id])
            )
        else:
            queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data_dict = request.data
        data_dict['organizer'] = request.user.id
        serializer = self.input_serializer_class(data=data_dict)
        serializer.is_valid(raise_exception=True)
        event = self.perform_create(serializer)
        output_serializer_class = self.get_serializer_class()
        event_data = output_serializer_class(event).data
        headers = self.get_success_headers(event_data)

        send_mail_notification(self.EMAIL_SUBJECT, event)

        return Response(event_data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        request.data['organizer'] = instance.organizer.id
        serializer = self.input_serializer_class(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        event = self.perform_update(serializer)
        output_serializer_class = self.get_serializer_class()
        event_data = output_serializer_class(event).data

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(event_data)

    def perform_update(self, serializer):
        return serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.organizer_id == request.user.id or request.user.is_superuser:
            self.perform_destroy(instance)
        else:
            participators = list(instance.participators.all().values_list('id', flat=True))
            try:
                del participators[participators.index(request.user.id)]
            except ValueError:
                return Response(status=status.HTTP_204_NO_CONTENT)
            participators_new = {'participators': participators}
            serializer = self.input_serializer_class(instance, data=participators_new, partial=True)
            serializer.is_valid(raise_exception=True)
            _ = self.perform_update(serializer)
        return Response(status=status.HTTP_204_NO_CONTENT)
