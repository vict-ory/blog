from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('delete-post/<str:ref>/', views.deletePost, name='delete-post'),
    path('update-post/<str:ref>/', views.updatePost, name='update-post'),
]