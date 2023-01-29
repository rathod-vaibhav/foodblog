from django.db import models

# Create your models here.

class Client(models.Model):
    #registration data given this table in enter
    email=models.EmailField(unique=True)
    username=models.CharField(max_length=30)
    password=models.CharField(max_length=30)
    gender=models.CharField(max_length=30)
    phonenumber=models.CharField(max_length=10)

    def __str__(self):
        return self.username
    
class Orders_Download(models.Model):
    person_name = models.CharField(max_length=20,default="demo")
    order_num= models.CharField(null=False,max_length=10)
    updated_on= models.DateField(auto_now_add=True)
    place_order = models.BooleanField(default=False)