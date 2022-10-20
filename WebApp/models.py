from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    emailid = models.EmailField(max_length=254)
    address = models.CharField(max_length=1024)
    city = models.CharField(max_length=1024)
    state = models.CharField(max_length=1024)
    pin_code = models.CharField(max_length=12)
    profile_pic = models.ImageField(null=True, blank=True)

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    emailid = models.EmailField(max_length=254)
    address = models.CharField(max_length=1024)
    city = models.CharField(max_length=1024)
    state = models.CharField(max_length=1024)
    pin_code = models.CharField(max_length=12)
    profile_pic = models.ImageField(null=True, blank=True)

