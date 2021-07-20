from django.db.models import Count
from rest_framework import serializers

from apps.posts.models import Post, Like


class PostSerializer(serializers.ModelSerializer):
    """
    Post's serializer
    """

    class Meta:
        model = Post
        fields = "__all__"


class LikeSerializer(serializers.ModelSerializer):
    """
    Like's serializer
    """

    class Meta:
        model = Like
        fields = "__all__"


class LikeAnalyticsSerializer(serializers.ModelSerializer):
    """
    Serializer for likes analytics
    """

    likes_count = serializers.SerializerMethodField('is_named_likes_count')

    class Meta:
        model = Like
        fields = ('created_date', 'likes_count')

    @staticmethod
    def is_named_likes_count(obj: Like) -> int:
        """
        Method filters users likes by created date and count it for the date
        :param obj: Like model object
        :return: int - likes count for the date
        """

        likes = Like.objects.filter(created_date=obj.created_date)
        return likes.count()
