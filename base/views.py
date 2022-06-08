from django.shortcuts import render
from django.http import HttpResponse, HttpRequest


def home(_: HttpRequest) -> HttpResponse:
    return render(None, 'home.html')
