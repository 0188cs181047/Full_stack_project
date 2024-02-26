from django.contrib import admin
from .models import Post ,CommentPost,Like ,ReplyPost ,Notification
# Register your models here.


admin.site.register(Post)
admin.site.register(CommentPost)
admin.site.register(Like)
admin.site.register(ReplyPost)

admin.site.register(Notification)