from django.conf import settings
from django.db import models


from django.contrib.auth.models import User
from django.utils import timezone

class Teacher(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    status= models.BooleanField(default=False)
    salary=models.PositiveIntegerField(null=True)
    
    
class CoursePublication(models.Model):
    student = models.ForeignKey('cridential.StudentUser', on_delete=models.CASCADE)
    course = models.ForeignKey('onlinexam.Course', on_delete=models.CASCADE)
    publication_date = models.DateTimeField(default=timezone.now)
    expiration_days = models.PositiveIntegerField(null=True, blank=True, default=None)
    expiration_hours = models.PositiveIntegerField(null=True, blank=True, default=None)
    is_attended = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.course} published to {self.student}"
    
    def set_expiration_time(self):
        if self.expiration_days is None and self.expiration_hours is None:
            return
        now = timezone.now()
        print(f"Expiration days: {self.expiration_days}, hours: {self.expiration_hours}")
        self.expiration_hours = int(self.expiration_hours) if self.expiration_hours else None
        delta = timezone.timedelta(days=self.expiration_days or 0, hours=self.expiration_hours or 0)
        self.expiration_date = now + delta
        self.save()
    
    def is_expired(self):
        now = timezone.now()
        return self.expiration_date is not None and self.expiration_date <= now
    
    def is_valid(self):
        return self.expiration_date is None or not self.is_expired()