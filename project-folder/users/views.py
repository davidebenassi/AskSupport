from django.shortcuts import render, redirect
from .forms import UserRegisterForm

def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('companies_home_page')
    else:
        form = UserRegisterForm()
    return render(request, 'register_user.html', {'form': form})