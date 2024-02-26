import re
from time import timezone
from django.db import models
from django.urls import reverse
from django.conf import settings

from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, AnonymousUser
from teacher.models import Teacher


# Create your models here.



from django.core.exceptions import ValidationError
from PIL import Image

class Post(models.Model):
    title = models.CharField(max_length=255)
    teacher = models.ForeignKey('cridential.TeacherUser', on_delete=models.CASCADE, null=True)
    video_file = models.FileField(upload_to='media/videos/', blank=True)
    posti = models.ImageField(upload_to='media/images/', null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='imageuser', on_delete=models.CASCADE, default='username')
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, default=None, blank=True, related_name='liked')
    description = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse('imagedetail', args=[self.id])

    def totol_likes(self):
        return self.liked.count()

    def comment_count(self):
        return CommentPost.objects.filter(video=self).count()

  
    
class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
class CommentPost(models.Model):
        video = models.ForeignKey(Post,null=True, on_delete=models.CASCADE)
        user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE ,null=True)
        content = models.TextField(max_length=160)
        mention = models.CharField(max_length=100, blank=True)
        timestamp = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return '{}-{}'.format(self.video.title,str(self.user.username))
        
        def count_reply(self):
             return ReplyPost.objects.filter(comment=self).count()
        
        def save(self, *args, **kwargs):
            pattern = r'@(?P<username>\w+)'
            mention_usernames = re.findall(pattern, self.content)
            self.mention = ','.join(set(mention_usernames))
            super().save(*args, **kwargs)


        
class ReplyPost(models.Model):
    comment = models.ForeignKey(CommentPost, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
    


class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications_sent', on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    target = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_at',)