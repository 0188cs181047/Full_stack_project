import django_filters
from .models import Recruiter,UploadedFile

class RecruiterFilter(django_filters.FilterSet):
    class Meta:
        model = Recruiter
        fields = ['Position','date_created','Priority','r_status']

class UploadedFileFilter(django_filters.FilterSet):
    class Meta:
        model = UploadedFile
        fields = ['experience', 'status','date_created']