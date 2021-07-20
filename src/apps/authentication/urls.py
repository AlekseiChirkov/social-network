from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.authentication.views import UserCreateAPIView, UserActivityListAPIView


urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='users_registration'),
    path('login/', TokenObtainPairView.as_view(), name='users_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('activity/', UserActivityListAPIView.as_view(), name='users_activity')
]
