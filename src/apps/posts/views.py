from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.posts.models import Post, Like
from apps.posts.serializers import (
    PostSerializer, LikeSerializer, LikeAnalyticsSerializer
)
from apps.posts.services import LikesAnalyticsService


class PostListCreateAPIView(ListCreateAPIView):
    """
    Class for posts creation
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AllowAny, )

    def list(self, request, *args, **kwargs):
        """
        Method returns list of posts
        :param request: WSGIRequest - method and url
        :param args: other args
        :param kwargs: other kwargs
        :return: response with status and data
        """

        posts = self.queryset.all()
        serializer = self.serializer_class(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs) -> Response:
        """
        Methods creates posts objects
        :param request: WSGIRequest - method and url
        :param args: other args
        :param kwargs: other kwargs
        :return: response with status and data
        """

        user = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LikeCreateAPIView(CreateAPIView):
    """
    Class for post's likes
    """

    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticated, )

    def create(self, request, *args, **kwargs) -> Response:
        """
        Method creates like for post
        :param request: WSGIRequest - method and url
        :param args: other args
        :param kwargs: other kwargs
        :return: response with status and data
        """
        user = request.user
        try:
            post = Post.objects.get(pk=self.kwargs.get("pk"))
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save(post=post, user=user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )


class LikeAnalyticsListAPIView(ListAPIView):
    """
    View for likes analytics
    """

    serializer_class = LikeAnalyticsSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self) -> Like:
        """
        Method returns Like queryset
        :return: Like queryset
        """

        return LikesAnalyticsService.get_likes_distinct_by_date(self.request)
