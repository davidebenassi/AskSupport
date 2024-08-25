from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def signup_page(request):
    return render(request, 'signup_page.html')