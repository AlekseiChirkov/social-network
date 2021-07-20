from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView, ListAPIView

from apps.authentication.models import User
from apps.authentication.serializers import (
    UserCreationSerializer, UserActivitySerializer
)


class UserCreateAPIView(CreateAPIView):
    """
    User registration view extended from generics CreateAPIView
    """

    serializer_class = UserCreationSerializer
    permission_classes = (AllowAny, )


class UserActivityListAPIView(ListAPIView):
    """
    User activity view extended from generics ListAPIView
    """

    queryset = User.objects.all()
    serializer_class = UserActivitySerializer
    permission_classes = (IsAuthenticated, )
