from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from base.forms import RegisterForm, NewCommentForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib import auth
from .models import Comment
from datetime import datetime
from django.contrib.auth import get_user_model


def home(request: HttpRequest) -> HttpResponse:
    # Posts to test layout & styling
    mock_posts = [
        Comment(
            publisher=get_user_model().objects.get(id=1),
            title='Test post',
            message='Test post body',
            publication_date=datetime.now()),
        Comment(
            publisher=get_user_model().objects.get(id=1),
            title='Hey, it\'s another Test post',
            message='talking about nothing in particular',
            publication_date=datetime(2021, 2, 15)),
        Comment(
            publisher=get_user_model().objects.get(id=1),
            title='Last of the test posts',
            message='Lorem ipsum dolor sit amet',
            publication_date=datetime(2020, 11, 10))]
    return render(request, 'home.html', {'posts': mock_posts})


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


def new_post(request: HttpRequest) -> HttpResponse:
    user = request.user  # type: ignore
    if not user.is_authenticated:
        return redirect('/login')

    if request.method == 'POST':
        form = NewCommentForm(request.POST)
        if form.is_valid():
            post = NewCommentForm(
                parent=None,
                publisher=user,
                title=form.cleaned_data.get('title'),
                message=form.cleaned_data.get('message'),
                publication_date=form.cleaned_data.get('publication_date'))

            post = post.save()

            return redirect(f'/post/{post.id}')

    else:
        form = NewCommentForm()

    return render(request, 'create_post.html', {'form': form})
