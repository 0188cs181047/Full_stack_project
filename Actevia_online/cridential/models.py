from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import random
import string
from django_otp.oath import totp
import base64
import os
from assetapp.models import Asset_inform
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings
from postapp.models import Post


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, app_name=None):
        if not username:
            raise ValueError('The Username field must be set')
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email)

        if not password:
            # Generate a random password based on username, email, and app name
            password = self.generate_random_password(app_name)

        user.set_password(password)
        user.save(using=self._db)
        
        if app_name:
            app, created = AppName.objects.get_or_create(name=app_name)
            user.app_names.add(app)
        
        return user


    def create_superuser(self, username, email, password=None, app_name=None):
        user = self.create_user(username, email, password, app_name)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def generate_random_password(self, app_name):
        # Generate a random password using a combination of letters, digits, and app name
        random_password = ''.join(random.choice(string.ascii_letters + string.digits + app_name) for _ in range(8))
        return random_password
    
    class Meta:
        swappable = "AUTH_USER_MODEL"






class AppName(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    otp_secret_key = models.CharField(max_length=64, null=True, blank=True)
    app_name = models.ManyToManyField(AppName) # Change the app_name field to ManyToManyField
    Asset_inform = models.ManyToManyField(Asset_inform, blank=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='customuser_set',
        related_query_name='customuser',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='customuser_set',
        related_query_name='customuser',
    )

    def save(self, *args, **kwargs):
        if not self.password:
            # Generate a random password based on username and email
            self.password = self._generate_random_password()

        return super().save(*args, **kwargs)

    def _generate_random_password(self):
        # Generate a random password using a combination of letters and digits
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))

    def __str__(self):
        return self.username
    
    def generate_otp_secret_key(self):
        self.otp_secret_key = base64.b32encode(os.urandom(10)).decode()
        self.save()

    def verify_otp(self, otp):
        return totp.verify(otp, self.otp_secret_key)
    

    
class StudentUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=False)
    post = models.ManyToManyField(Post, blank=True, related_name='students')
    is_eligible = models.BooleanField(default=True)


    def __str__(self):
        return self.user



class TeacherUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher_profile')
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=False)
    status = models.BooleanField(default=False)
    salary = models.PositiveIntegerField(null=True)

    def __str__(self):
        return str(self.user.username)


 

