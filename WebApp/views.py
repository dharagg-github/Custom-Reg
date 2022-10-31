from django.contrib.auth import login, logout,authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import CreateView
from .form import PatientSignUpForm, DoctorSignUpForm, PostForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Post, Category, Doctor, Patient
from django.views.generic import ListView,DetailView,CreateView

import datetime
from datetime import timedelta
import pytz
from apiclient.discovery import build
import pickle


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

def listdoctor(request):
    form = []
    for doctor in Doctor.objects.all():
        if doctor.user.is_doctor:
            usr = {"first_name": doctor.user.first_name, "last_name": doctor.user.last_name, "profile_pic": doctor.profile_pic, "id":request.user.id, "did":doctor.user.id}
            form.append(usr)

    print(form)

    return render(request,'listdoctor.html',{'form':form})


def bookform(request, pk):
    form = Patient.objects.get(user_id=pk)
    if request.method == 'POST':
        form = Doctor.objects.get(user_id=5)
        print(form)
        req = request.POST['req']
        start = request.POST['start']
        time = request.POST['time']
        starts = start + ' ' + time + ':' '00'

        start_time = datetime.datetime.strptime(starts, "%Y-%m-%d %H:%M:%S")
        end_time = start_time + timedelta(minutes=45)
        context = {'req': req, 'start': start, 'time': time, 'start_time': start_time, 'end_time': end_time,
                   'form': form}
        return render(request, 'confirm.html', context)

    return render(request, 'bookform.html', {'form': form})


start_time = 0
end_time = 0

scopes = ['https://www.googleapis.com/auth/calendar']

credentials = pickle.load(open('C:\\Users\\DHARANEESH GG\\PycharmProjects\\CustomRegLog\\token.pkl', 'rb'))

def confirm(request):
    service = build("calendar", "v3", credentials=credentials)
    if request.method == 'POST':
        req = request.POST['required']
        start = request.POST['starts']
        time = request.POST['time']
        start = start + ' ' + time + ':' '00'
        start_time = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
        end_time = start_time + timedelta(minutes=45)
        timezone = 'Asia/Kolkata'
        print("Gsfgfd", start_time.isoformat(), 'vdfdf', end_time.isoformat())
        print("dsdv", req)
        event = (
            service.events()
                .insert(
                calendarId="primary",
                body={
                    "summary": req,

                    "start": {"dateTime": start_time.isoformat(),
                              'timeZone': timezone,

                              },
                    "end": {
                        "dateTime": end_time.isoformat(),
                        'timeZone': timezone,
                    }
                },
            )
                .execute()
        )

        return redirect('patient')

    return render(request, 'confirm.html')

def viewevent(request):
    service = build("calendar", "v3", credentials=credentials)
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        return

        # Prints the start and name of the next 10 events
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        email = event['attendees'][0:]
        print(start,email)

    return render(request,'viewevent.html',{'form':start})

def logout_view(request):
    logout(request)
    return redirect('/')



