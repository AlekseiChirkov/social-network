from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

from apps.authentication.models import User


class UpdateLastActivityMiddleware(MiddlewareMixin):
    @staticmethod
    def process_view(request, *args, **kwargs) -> None:
        """
        Method updates last activity field for User
        :param request: WSGIRequest - method and url
        :param args: other arguments
        :param kwargs: other keyword arguments
        :return: None
        """

        assert hasattr(request, 'user')
        if request.user.is_authenticated:
            (
                User.objects
                .filter(id=request.user.id)
                .update(last_activity=timezone.now())
            )
