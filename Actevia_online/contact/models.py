from django.db import models
from datetime import datetime
# Create your models here.

class Contact(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.now)

    class Meta:

        verbose_name = 'Conatact'
        verbose_name_plural = 'Conatcts'
    
    def __str__(self):
        return self.email