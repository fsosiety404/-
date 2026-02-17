from django.db import models

class Users(models.Model):
    user_name = models.CharField(max_length=45, unique=True)
    email_user = models.EmailField(unique=True, max_length=6000)
    created_dat = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=6000)
    salt_password = models.CharField(max_length=1000)
    bio_user = models.CharField(max_length=3500)
