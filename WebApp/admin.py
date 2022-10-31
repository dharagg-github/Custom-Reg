from django.contrib import admin
from .models import User, Patient, Doctor, Post, Category, Book

admin.site.register(User)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Book)
