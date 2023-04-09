from django.db import models

# Create your models here.
class AdminSetting(models.Model):
    header_image=models.ImageField(upload_to='media/', null=True, blank=True)
    payment_charge=models.FloatField(blank=True, null=True)
    
