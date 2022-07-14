from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('post/create', views.create_post, name='create_post'),
    path('post/view/<int:id>', views.view_post, name='view_post'),
    path('post/reply/<int:id>', views.reply_post, name='reply_post'),
    path('post/delete/<int:id>', views.delete_post, name='delete_post'),
    path('post/edit/<int:id>', views.edit_post, name='edit_post'),
    path('post/upvote/<int:id>', views.upvote_post, name='upvote_post'),
    path('post/downvote/<int:id>', views.downvote_post, name='downvote_post'),
    path('user/view/<int:id>', views.user_profile, name='user_profile'),
    path('', include('django.contrib.auth.urls')),
]