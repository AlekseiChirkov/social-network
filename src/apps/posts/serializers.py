from django.db.models import Count
from rest_framework import serializers

from apps.posts.models import Post, Like


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"


class LikeAnalyticsSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField('is_named_likes_count')

    class Meta:
        model = Like
        fields = ('created_date', 'likes_count')

    def is_named_likes_count(self, obj):
        likes = Like.objects.filter(created_date=obj.created_date)
        return likes.count()
