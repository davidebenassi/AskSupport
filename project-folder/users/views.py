from .forms import UserSignupForm
from django.views.generic import FormView
from django.urls import reverse_lazy

class UserSignupView(FormView):
    form_class = UserSignupForm
    template_name = 'user_signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)