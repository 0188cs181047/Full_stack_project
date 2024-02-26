from django.db import models

class Policy(models.Model):
    policy_name = models.CharField(max_length=200)
    upload_files = models.ManyToManyField('Upload', blank=True)

class Upload(models.Model):
    file = models.FileField()

