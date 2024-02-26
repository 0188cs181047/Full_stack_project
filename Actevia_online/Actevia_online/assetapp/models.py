from django.db import models
from django.forms import SelectDateWidget

class Asset_inform(models.Model):
    BOOKED = 'Pending'
    APPROVED = 'Approved'

    STATUS_TYPE = (
        (BOOKED, 'Pending'),
        (APPROVED, 'Approved')
    )
    
    asset_id = models.CharField(max_length=100)
    asset_photo = models.ImageField(upload_to='media/images/', null=True, blank="True")
    asset_owner = models.CharField(max_length=100)
    asset_type = models.CharField(max_length=200)
    Asset_date = models.DateTimeField(auto_now_add=True)
    asset_status = models.CharField(max_length=20, choices=STATUS_TYPE,null=True)

    def __str__(self):
        return str(self.asset_id)
    

    
