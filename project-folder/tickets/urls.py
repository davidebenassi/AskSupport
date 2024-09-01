from django.urls import path
from .views import *

urlpatterns = [
    path('accept-ticket/<int:ticket_id>/', accept_ticket, name='accept-ticket'),
    path('close-ticket/<int:ticket_id>/', close_ticket, name='close-ticket'),
]
