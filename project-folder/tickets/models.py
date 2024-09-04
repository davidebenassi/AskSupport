from django.db import models
from django.contrib.auth.models import User
from users.models import UserProfile

from companies.models import Company, EmployeeProfile

class Ticket(models.Model):
    OPEN = 'Open'
    CLOSED = 'Closed'
    PENDING = 'Pending'

    STATUS_CHOICES = [
        (OPEN, 'Open'),
        (CLOSED, 'Closed'),
        (PENDING, 'Pending')
    ]

    NONE = 0
    MEDIUM = 1
    HIGH = 2
    CRITIC = 3

    PRIORITY = [
        (NONE, 'None'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
        (CRITIC, 'Critic')
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='created_tickets')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='tickets')
    assigned_employee = models.ForeignKey(EmployeeProfile, on_delete=models.SET_NULL, related_name='tickets', null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    close_reason = models.TextField(null=True, blank=True)
    priority = models.IntegerField(choices=PRIORITY, default=NONE)

    def __str__(self):
        return f"Ticket #{self.id} - {self.title} ({self.status})"
    
    def get_messages(self):
        return self.messages.order_by('timestamp')
    
    def get_priority(self):
        return dict(self.PRIORITY).get(self.priority, 'Unknown')

class Message(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.sender.username} on Ticket #{self.ticket.id} - {self.timestamp}"