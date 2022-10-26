from django.contrib.auth import login, logout,authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import CreateView
from .form import PatientSignUpForm, DoctorSignUpForm, PostForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Post, Category, Doctor
from django.views.generic import ListView,DetailView,CreateView

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

class patient(ListView):
    model = Post
    template_name = '../templates/patient.html'

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(patient, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context

class doctor(ListView):
    model = Post
    template_name = '../templates/doctor.html'

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(doctor, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context

def CategorydView(request, cats):
    category_posts = Post.objects.filter(category=cats)
    return render(request,'../templates/categoryd.html',{'cats':cats.title(), 'category_posts':category_posts})

def CategorypView(request, cats):
    category_posts = Post.objects.filter(category=cats)
    return render(request,'../templates/categoryp.html',{'cats':cats.title(), 'category_posts':category_posts})

class myblog(ListView):
    model = Post
    template_name = '../templates/myblog.html'

    def get_queryset(self):
        user = Doctor()
        user.user = self.request.user
        return Post.objects.filter(author=user)

class article(DetailView):
    model = Post
    template_name = '../templates/article.html'

class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = '../templates/createblog.html'

def logout_view(request):
    logout(request)
    return redirect('/')



