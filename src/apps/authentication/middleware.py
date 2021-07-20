from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

from apps.authentication.models import User


class UpdateLastActivityMiddleware(MiddlewareMixin):
    def process_view(self, request, *args, **kwargs):
        assert hasattr(request, 'user')
        if request.user.is_authenticated:
            (
                User.objects
                .filter(id=request.user.id)
                .update(last_activity=timezone.now())
            )
