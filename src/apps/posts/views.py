from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.posts.models import Post
from apps.posts.serializers import (
    PostSerializer, LikeSerializer, LikeAnalyticsSerializer
)
from apps.posts.services import LikesAnalyticsService


class PostCreateAPIView(CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LikeCreateAPIView(CreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticated, )

    def create(self, request, *args, **kwargs):
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
    serializer_class = LikeAnalyticsSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        return LikesAnalyticsService.get_likes_distinct_by_date(self.request)
