from django.contrib import admin

# Register your models here.

from .models import Student ,VideoPublication

admin.site.register(Student)
admin.site.register(VideoPublication)

