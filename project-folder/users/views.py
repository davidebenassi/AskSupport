from .forms import UserSignupForm
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render

from tickets.models import Ticket 

class UserSignupView(FormView):
    form_class = UserSignupForm
    template_name = 'user_signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
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

