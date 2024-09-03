from django.views import View
from .forms import *
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView

from tickets.models import Ticket 
from .models import UserProfile

class UserSignupView(FormView):
    form_class = UserSignupForm
    template_name = 'user_signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
@login_required
def user_tickets(request):
    userProfile = request.user.related_profile
    tickets = Ticket.objects.filter(created_by=userProfile)

    return render(request, 'user_tickets_page.html', context = {
        'open_tickets': tickets.filter(status=Ticket.OPEN),
        'pending_tickets' : tickets.filter(status=Ticket.PENDING),
        'closed_tickets' : tickets.filter(status=Ticket.CLOSED)
        }
    )

class UserProfileView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'user_profile.html'
    
    def get_object(self):
        # Restituisce il profilo dell'utente loggato
        return self.request.user.related_profile

class UpdateUserProfileView(LoginRequiredMixin, View):
    template_name = 'update_user_profile.html'
    success_url = reverse_lazy('user-profile')

    def get(self, request, *args, **kwargs):
        user_form = EditUserProfileForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.related_profile)

        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form,
        })

    def post(self, request, *args, **kwargs):
        user_form = EditUserProfileForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.related_profile)

        if user_form.is_valid():
            user_form.save()

        if profile_form.is_valid():
            profile_form.save()

        return redirect(self.success_url)

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_url = reverse_lazy('user-profile')

class DeleteProfileView(LoginRequiredMixin, FormView):
    template_name = 'delete_profile_confirmation.html'
    form_class = ConfirmPasswordForm
    success_url = reverse_lazy('home')  # O un'altra pagina dopo la cancellazione

    def form_valid(self, form):
        password = form.cleaned_data['password']
        user = authenticate(username=self.request.user.username, password=password)

        if user is not None:
            user.delete()  # Elimina User e il suo UserProfile correlato
            logout(self.request)  # Disconnetti l'utente dopo l'eliminazione
            return super().form_valid(form)
        else:
            form.add_error('password', 'Incorrect password.')
            return self.form_invalid(form)