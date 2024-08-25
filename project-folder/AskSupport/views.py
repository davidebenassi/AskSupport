from django.shortcuts import render

def signup_page(request):
    return render(request, 'signup_page.html')