from django.db import models
from django.conf import settings

from django.contrib.auth.models import User
from postapp.models import Post

class Student(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    post = models.ManyToManyField(Post, blank=True)
    is_eligible = models.BooleanField(default=True)
   
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name
    
class VideoPublication(models.Model):
    student = models.ForeignKey('cridential.StudentUser', on_delete=models.CASCADE)
    video_file = models.ForeignKey(Post, on_delete=models.CASCADE)
    published_at = models.DateTimeField(auto_now_add=True)









