from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from base.forms import RegisterForm, PostForm, ReplyForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib import auth
from .models import Comment
from django.contrib.auth import get_user_model


def home(request: HttpRequest) -> HttpResponse:
    posts = Comment.objects.all()  # type: ignore
    return render(request, 'home.html', {'posts': posts})


# Attempts to sign up user on POST, renders registration page otherwise
def register(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Save new user to DB, return model instance
            user = form.save()
            # Authenticate the user for the current session
            auth.login(request, user)
            # Flash 'success' message after redirect
            messages.success(request, 'Account created successfully')
            # Redirect to home
            return redirect('home')
    else:
        # No previous form data, proceed with empty form
        form = RegisterForm()
    # Render registration view with empty or invalid form
    return render(request, 'registration/register.html', {'form': form})


def login(request: HttpRequest) -> HttpResponse:
    status = 200
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        print(form.is_valid(), form.errors)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                messages.success(
                    request=request,
                    message=f'Logged in as {username}')
                return redirect('home')
        messages.error(request=request, message='Invalid username or password')
        status = 400
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html',
                  {'form': form}, status=status)


def create_post(request: HttpRequest) -> HttpResponse:
    user = request.user  # type: ignore
    if not user.is_authenticated:
        return redirect('/login')

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = Comment(**form.cleaned_data, publisher=user, parent=None, original_post=None)
            post.save()
            return redirect('view_post', id=post.id)  # type: ignore

    else:
        form = PostForm()

    return render(request, 'create-post.html', {'form': form})

def reply_post(request: HttpRequest, id) -> HttpResponse:
    user = request.user # type: ignore
    parent = Comment.objects.get(id=id) # type: ignore
    (original_post, replies) = get_original_post_and_replies(id)

    if not user.is_authenticated:
        return redirect('/login')

    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            post = Comment(**form.cleaned_data, publisher=user, parent=parent, original_post=original_post, title=None)
            post.save()
            return redirect('view_post', id=original_post.id)
    else:
        form = ReplyForm()

    return render(request, 'view-post.html', {'form':form, 'replies':replies, 'post':original_post, 'parent':parent})



def view_post(request: HttpRequest, id) -> HttpResponse:
    (original_post, replies) = get_original_post_and_replies(id)
    return render(request, 'view-post.html', {'post': original_post, 'replies':replies})  # type: ignore


def delete_post(request: HttpRequest, id) -> HttpResponse:
    user = request.user  # type: ignore
    post = Comment.objects.get(id=id)  # type: ignore
    if not user.is_authenticated:
        messages.error(
            request,
            'You need to be logged in to perform this action')
    elif not post:
        messages.error(request, 'This post does not exist')
    elif post.publisher != user:
        messages.error(request, 'You cannot delete someone elses post')
    else:
        post.delete()
        messages.success(request, 'Post deleted')
    return redirect('home')


def edit_post(request: HttpRequest, id) -> HttpResponse:
    return HttpResponse('unimplemented')


def user_profile(request: HttpRequest, id) -> HttpResponse:
    user = get_user_model().objects.get(id=id)
    if not user:
        messages.error(request, 'This user does not exist')
        return redirect('home')
    return render(request, 'user-profile.html', {'user': user})


def get_original_post_and_replies(post_id):
    post = Comment.objects.get(id=post_id) # type: ignore
    original_post = None
    if post.parent == None:
        original_post = post
    elif post.parent.original_post == None:
        original_post = post.parent
    else:
        original_post = parent.original_post
    replies = original_post.replies.all()

    return (original_post, replies)



