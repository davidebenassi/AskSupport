from .forms import UserSignupForm
from .models import UserProfile
#from django.contrib.auth import login
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

class UserSignupView(CreateView):
    model = UserProfile
    form_class = UserSignupForm
    template_name = 'user_signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # Salva l'utente e fai login
        user = form.save()
        #login(self.request, user)
        return super().form_valid(form)