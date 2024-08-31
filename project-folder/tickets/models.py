from django.db import models
from django.contrib.auth.models import User
from users.models import UserProfile

from companies.models import Company, EmployeeProfile

class Ticket(models.Model):
    OPEN = 'open'
    CLOSED = 'closed'
    PENDING = 'pending'

    STATUS_CHOICES = [
        (OPEN, 'Open'),
        (CLOSED, 'Closed'),
        (PENDING, 'Pending')
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='created_tickets')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='tickets')
    assigned_employee = models.ForeignKey(EmployeeProfile, on_delete=models.SET_NULL, related_name='tickets', null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ticket #{self.id} - {self.title} ({self.status})"
    
    def get_messages(self):
        return self.messages.order_by('timestamp')

class Message(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.sender.user.username} on Ticket #{self.ticket.id} - {self.timestamp}"