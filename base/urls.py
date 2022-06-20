from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('new_post/', views.new_post, name='new_post'),
    path('', include('django.contrib.auth.urls')),
]
