from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from .models import Ticket
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def is_employee(user):
    return user.groups.filter(name='Employees').exists()

@user_passes_test(is_employee)
def accept_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.user.employee_profile.company != ticket.company:
        raise PermissionDenied("You don't have permissions to manage this ticket.")

    ticket.status = Ticket.OPEN
    ticket.assigned_employee = request.user.employee_profile
    ticket.save()
    

    return redirect(reverse('employee-dashboard'))

@user_passes_test(is_employee)
def close_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.user.employee_profile.company != ticket.company:
        raise PermissionDenied("You don't have permissions to manage this ticket.")

    
    if request.method == "POST":
        close_reason = request.POST.get('close_reason')
    
        ticket.status = Ticket.CLOSED
        ticket.close_reason = close_reason
        
        ticket.save()

    return redirect(reverse('employee-dashboard'))
