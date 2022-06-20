from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from base.forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib import auth


def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'home.html')


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
            # Form is invalid, flash errors from form validators
            messages.error(request, form.errors)
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
                messages.info(
                    request=request,
                    message=f'Logged in as {username}')
                return redirect('home')
        messages.error(request=request, message='Invalid username or password')
        status = 400
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html',
                  {'form': form}, status=status)
