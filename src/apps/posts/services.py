from apps.posts.models import Like


class LikesAnalyticsService:
    @staticmethod
    def get_likes_distinct_by_date(request):
        user = request.user
        from_date = request.query_params['from']
        to_date = request.query_params['to']
        qs = Like.objects.filter(
            created_date__range=[from_date, to_date],
            user=user,
        )
        return qs.distinct('created_date')
