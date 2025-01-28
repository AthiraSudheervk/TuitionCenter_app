from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    user_type=models.CharField(default=1,max_length=255)
    status=models.IntegerField(default=0)

class Teachers(models.Model):
    User=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    Age=models.IntegerField(null=True)
    Phone_number=models.CharField(max_length=255,null=True)
    Course=models.CharField(max_length=255,null=True)
    Image=models.ImageField(upload_to="images/",null=True,blank=True)

class Students(models.Model):
    User=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    Age=models.IntegerField(null=True)
    Phone_number=models.CharField(max_length=255,null=True)
    Course=models.CharField(max_length=255,null=True)
    Image=models.ImageField(upload_to="images/",null=True,blank=True)