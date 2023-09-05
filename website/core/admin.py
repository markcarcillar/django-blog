from django.contrib import admin

from .models import BlogModel, CommentModel, LikeModel

admin.site.register(BlogModel)
admin.site.register(CommentModel)
admin.site.register(LikeModel)