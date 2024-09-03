from django.urls import path
from .views import *

urlpatterns = [
    path('accept-ticket/<int:ticket_id>/', accept_ticket, name='accept-ticket'),
    path('close-ticket/<int:ticket_id>/', close_ticket, name='close-ticket'),

    path('<int:ticket_id>/messages/', get_ticket_messages, name='get-ticket-messages'),
    path('<int:ticket_id>/send_message/', send_message, name='send-message'),
]
