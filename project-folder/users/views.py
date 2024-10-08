from .forms import *
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, DetailView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView

from tickets.models import Ticket 
from .models import UserProfile

class UserSignupView(FormView):
    form_class = UserSignupForm
    template_name = 'user_signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user, _ = form.save()
        login(self.request, user)
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
        return self.request.user.related_profile

class UpdateUserProfileView(LoginRequiredMixin, View):
    template_name = 'update_user_profile.html'
    success_url = reverse_lazy('user-profile')

    def get(self, request, *args, **kwargs):
        user_form = EditUserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.related_profile)

        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form,
        })

    def post(self, request, *args, **kwargs):
        user_form = EditUserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.related_profile)

        if user_form.is_valid():
            user_form.save()

        if profile_form.is_valid():
            profile_form.save()

        return redirect(self.success_url)

class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_url = reverse_lazy('user-profile')

class DeleteProfileView(LoginRequiredMixin, FormView):
    template_name = 'delete_confirmation.html'
    form_class = ConfirmPasswordForm
    success_url = reverse_lazy('home')  

    def form_valid(self, form):
        password = form.cleaned_data['password']
        user = authenticate(username=self.request.user.username, password=password)

        if user is not None:
            user.delete()  
            logout(self.request)  
            return super().form_valid(form)
        else:
            form.add_error('password', 'Incorrect password.')
            return self.form_invalid(form)