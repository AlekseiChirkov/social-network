from django.contrib import admin

from apps.posts.models import Like, Post


admin.site.register(Like)
admin.site.register(Post)
