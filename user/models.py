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