from .forms import UserSignupForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

class UserSignupView(CreateView):
    form_class = UserSignupForm
    template_name = 'user_signup.html'
    success_url = reverse_lazy('login')