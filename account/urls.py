from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.register, name='register'),
    path('login/', views.loginuser, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('newsltter/', views.createNewsletter, name='newsletter'),
    path('send-newsltter/', views.sendNewsletter, name='send-newsletter'),
    path('forget-password/', views.forgetPassword, name='forget-password'),
    path('forget-password/code/<str:ref>/', views.code, name='code'),
    path('new-password/<str:ref>/', views.newPassword, name='new-password'),
]