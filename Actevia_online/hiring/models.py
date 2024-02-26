from django.db import models
from django.contrib.admin.widgets import AdminSplitDateTime
import random
import string
from datetime import datetime 
from django.core.validators import FileExtensionValidator
import os


r_status = (
    ("Open", "Open"),
    ("Closed", "Closed"),
    ("Freeze", "Freeze")
)

Priority = (
    ("High", "High"),
    ("Low", "Low"),
)

onboarding_status = (
    ("Offered", "Profile Selected"),
    ("Rejected", "Profile Rejected"),
    ("OnHold", "Yet to upload to the client"),
)

class Recruiter(models.Model):
    companyname = models.CharField(max_length=30)
    job_id = models.CharField(max_length=12, unique=True, null=True, blank=True)
    Position = models.CharField(max_length=30)
    resourcerequired = models.FloatField()
    jd = models.TextField()
    resourceremaining = models.FloatField()
    r_status = models.CharField(max_length=20 , choices=r_status , default="open")
    date_created = models.DateField(auto_now=True)
    Priority = models.CharField(max_length=30, choices=Priority , default="High")
    class Meta:
        db_table = "resources"

    # def __str__(self):
    #     return self.job_id
    def __str__(self):
        return self.job_id or ""
    
    def save(self, *args, **kwargs):
        if not self.pk:
            # generate job id if it's a new record
            random_suffix = ''.join(random.choices(string.digits, k=6))
            self.job_id = self.companyname[:5].upper() + random_suffix
        super().save(*args, **kwargs)




class UploadedFile(models.Model):
    job_id = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    candidate_name = models.CharField(max_length=30)
    contact = models.CharField(max_length=20)
    experience = models.CharField(max_length=4)
    owner_name = models.CharField(max_length=30)
    l1 = models.CharField(max_length=30)
    l2 = models.CharField(max_length=30)
    l3 = models.CharField(max_length=30)
    status = models.CharField(max_length=20, choices=onboarding_status, default="OnHold")
    date_created = models.DateField(auto_now=True)

    class Meta:
        db_table = "uploaded_files"


class Company(models.Model):
    name = models.CharField(max_length=100)

class CompanyData(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    experience = models.IntegerField()
    band = models.CharField(max_length=10)
    ctc = models.CharField(max_length=20)

