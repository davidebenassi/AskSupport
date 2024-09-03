from .forms import *
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from tickets.models import Ticket 

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

@login_required
def profile_view(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.related_profile)
        password_form = PasswordChangeFormCustom(user=request.user, data=request.POST)

        if user_form.is_valid() and profile_form.is_valid() and (not password_form.has_changed() or password_form.is_valid()):
            user_form.save()
            profile_form.save()
            
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Keeps the user logged in after changing the password

            return redirect('profile')  # Redirect to the same page or another page

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.related_profile)
        password_form = PasswordChangeFormCustom(user=request.user)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form,
    }
    return render(request, 'profile.html', context)