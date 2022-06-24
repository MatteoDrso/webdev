from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('post/create', views.new_post, name='new_post'),
    path('post/view/<int:id>', views.view_post, name='view_post'),
    path('post/delete/<int:id>', views.delete_post, name='delete_post'),
    path('post/edit/<int:id>', views.edit_post, name='edit_post'),
    path('', include('django.contrib.auth.urls')),
]
