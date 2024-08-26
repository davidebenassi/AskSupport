from .forms import UserSignupForm
from django.views.generic.edit import CreateView
from django.shortcuts import render
from django.urls import reverse_lazy

class UserSignupView(CreateView):
    form_class = UserSignupForm
    template_name = 'user_signup.html'
    success_url = reverse_lazy('login')




'''from django.shortcuts import render, redirect
from .forms import UserRegisterForm

def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('companies_home_page')
    else:
        form = UserRegisterForm()
    return render(request, 'register_user.html', {'form': form})'''