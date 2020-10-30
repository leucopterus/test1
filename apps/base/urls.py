from django.urls import path

from .views import (
    MyTokenObtainPairView,
    MyTokenRefreshView,
    RegisterView,
)


urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view({'post': 'create'}), name='register'),
]
