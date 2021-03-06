from django.urls import path

from apps.posts.views import (
    LikeCreateAPIView, PostListCreateAPIView, LikeAnalyticsListAPIView
)


urlpatterns = [
    path('<int:pk>/like/', LikeCreateAPIView.as_view(), name='create_like'),
    path('post/', PostListCreateAPIView.as_view(), name='create_post'),
    path('likes-count/', LikeAnalyticsListAPIView.as_view(),
         name='likes_analytics'),
]
