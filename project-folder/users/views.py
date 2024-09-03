from .forms import *
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView, DeleteView
from django.http import Http404

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

    # Filtra i ticket in base all'utente loggato
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

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    template_name = 'edit_profile.html'
    form_class = UserProfileForm
    second_form_class = UserForm
    success_url = reverse_lazy('user-profile')

    def get_object(self):
        return self.request.user.related_profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'user_form' not in context:
            context['user_form'] = self.second_form_class(instance=self.request.user)
        if 'profile_form' not in context:
            context['profile_form'] = self.form_class(instance=self.request.user.related_profile)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_form = UserForm(request.POST, instance=self.request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=self.request.user.related_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return self.form_valid(profile_form)
        else:
            return self.form_invalid(user_form)
        

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