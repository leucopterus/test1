from rest_framework.routers import DefaultRouter

from apps.event.views import EventViewSet

router = DefaultRouter()
router.register('', EventViewSet, basename='events')

urlpatterns = eventpatterns = router.urls
