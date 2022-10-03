from django.db import models

# Create your models here.
class Users(models.Model):
    user_username = models.CharField(max_length=20)
    user_password = models.CharField(max_length=40)

