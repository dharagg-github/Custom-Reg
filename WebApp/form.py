from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import User,Patient,Doctor, Post, Category



class PatientSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    emailid = forms.EmailField(required=True)
    address = forms.CharField(required=True)
    city = forms.CharField(required=True)
    state = forms.CharField(required=True)
    pin_code = forms.CharField(required=True)
    profile_pic = forms.ImageField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_patient = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        patient = Patient.objects.create(user=user)
        patient.emailid = self.cleaned_data.get('emailid')
        patient.address = self.cleaned_data.get('address')
        patient.city = self.cleaned_data.get('city')
        patient.state = self.cleaned_data.get('state')
        patient.pin_code = self.cleaned_data.get('pin_code')
        patient.profile_pic = self.cleaned_data.get('profile_pic')
        patient.save()
        return user


class DoctorSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    emailid = forms.EmailField(required=True)
    address = forms.CharField(required=True)
    city = forms.CharField(required=True)
    state = forms.CharField(required=True)
    pin_code = forms.CharField(required=True)
    profile_pic = forms.ImageField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_doctor = True
        user.is_staff = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        doctor = Doctor.objects.create(user=user)
        doctor.emailid = self.cleaned_data.get('emailid')
        doctor.address = self.cleaned_data.get('address')
        doctor.city = self.cleaned_data.get('city')
        doctor.state = self.cleaned_data.get('state')
        doctor.pin_code = self.cleaned_data.get('pin_code')
        doctor.profile_pic = self.cleaned_data.get('profile_pic')
        doctor.save()
        return user

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','author','category','summary','draft','content')

        widget = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'summary': forms.TextInput(attrs={'class': 'form-control'}),
            'draft': forms.BooleanField(),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }