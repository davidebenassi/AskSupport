from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from .models import Ticket, Message
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse


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

@login_required
def get_ticket_messages(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # * Check if the message sender is the creator or the assigned employee * #
    if hasattr(request.user, 'related_profile') and request.user.related_profile == ticket.created_by:
        is_authorized = True
    elif hasattr(request.user, 'employee_profile') and request.user.employee_profile == ticket.assigned_employee:
        is_authorized = True
    else:
        is_authorized = False

    if not is_authorized:
        return JsonResponse({'error': 'Permission denied'}, status=403)

    messages = ticket.get_messages().values('sender__username', 'content', 'timestamp')
    messages = list(messages)
    return JsonResponse({'messages': messages})

@login_required
def send_message(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)


    # * Check if the message sender is the creator or the assigned employee * #
    if hasattr(request.user, 'related_profile') and request.user.related_profile == ticket.created_by:
        is_authorized = True
    elif hasattr(request.user, 'employee_profile') and request.user.employee_profile == ticket.assigned_employee:
        is_authorized = True
    else:
        is_authorized = False

    if not is_authorized:
        return JsonResponse({'error': 'Permission denied'}, status=403)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(ticket=ticket, sender=request.user, content=content)
            return JsonResponse({'success': True})

    return JsonResponse({'success': False})