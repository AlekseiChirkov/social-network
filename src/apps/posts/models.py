from django.db import models


class Post(models.Model):
    creator = models.ForeignKey(
        'authentication.User', on_delete=models.CASCADE, blank=True, null=True
    )
    title = models.CharField(max_length=128)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)


class Like(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, blank=True,  null=True,
        related_name='likes'
    )
    user = models.ForeignKey(
        'authentication.User', on_delete=models.SET_NULL, blank=True, null=True,
        related_name='likes'
    )
    created_date = models.DateField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.user.first_name + "'s like"
