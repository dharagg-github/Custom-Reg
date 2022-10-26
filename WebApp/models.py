from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from ckeditor.fields import RichTextField


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

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('doctor')

class Post(models.Model):
    title = models.CharField(max_length=255)

    summary = models.TextField()
    author = models.ForeignKey(Doctor, on_delete= models.CASCADE)
    content = RichTextField(blank=True,null=True)
    choices = Category.objects.all().values_list('name', 'name')
    # choice = [('Mental Health','Mental Health'),('Heart Disease','Heart Disease'),('Covid19','Covid19'),('Immunization','Immunization'),]

    choice_list = []
    for item in choices:
        choice_list.append(item)

    category = models.CharField(max_length=255,choices=choices)
    draft = models.BooleanField(default=False)

    def __str__(self):
        return self.title + ' | ' + str(self.author)
    def get_absolute_url(self):
        return reverse('doctor')

