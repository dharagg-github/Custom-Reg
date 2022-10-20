from django.contrib.auth import login, logout,authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import CreateView
from .form import PatientSignUpForm, DoctorSignUpForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User

def index(request):
    return render(request, '../templates/index.html')

def register(request):
    return render(request, '../templates/register.html')

class patient_register(CreateView):
    model = User
    form_class = PatientSignUpForm
    template_name = '../templates/patient_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('patient')


class doctor_register(CreateView):
    model = User
    form_class = DoctorSignUpForm
    template_name = '../templates/doctor_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('doctor')

def login_request(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_patient:
                login(request,user)
                return redirect('patient')
            elif user is not None and user.is_doctor:
                login(request,user)
                return redirect('doctor')
            else:
                messages.error(request,"Invalid username or password")
        else:
                messages.error(request,"Invalid username or password")
    return render(request, '../templates/login.html',
    context={'form':AuthenticationForm()})

def patient(request):
    return render(request, '../templates/patient.html')

def doctor(request):
    return render(request, '../templates/doctor.html')

def logout_view(request):
    logout(request)
    return redirect('/')



