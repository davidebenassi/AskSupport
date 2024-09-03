from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='user_signup'),
    path('tickets/', user_tickets, name='user-tickets'),
    path('profile/', profile_view, name='user-profile'),
]