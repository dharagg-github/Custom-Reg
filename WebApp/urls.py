from django.urls import path
from . import views
from .views import doctor,article,patient,AddPostView,myblog

urlpatterns = [
    path('', views.index, name='index'),
    path('register/',views.register, name='register'),
    path('patient_register/',views.patient_register.as_view(), name='patient_register'),
    path('doctor_register/',views.doctor_register.as_view(), name='doctor_register'),
    path('login/', views.login_request, name='login'),
    path('patient/', patient.as_view(), name='patient'),
    path('doctor/', doctor.as_view(), name='doctor'),
    path('article/<int:pk>', article.as_view(), name='article'),
    path('add_post/', AddPostView.as_view(), name='add_post'),
    path('categoryd/<str:cats>/',views.CategorydView,name= 'categoryd'),
    path('categoryp/<str:cats>/',views.CategorypView,name= 'categoryp'),
    path('myblog/', myblog.as_view(), name='myblog'),
    path('listdoctor/', views.listdoctor, name='listdoctor'),
    path('bookform/<str:pk>/', views.bookform, name='bookform'),
    path('confirm', views.confirm, name='confirm'),
    path('viewevent', views.viewevent, name='viewevent'),
    path('logout/', views.logout_view, name='logout'),

]