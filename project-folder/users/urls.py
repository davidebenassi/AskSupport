from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='user_signup'),
    path('tickets/', user_tickets, name='user-tickets'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/edit/', UpdateUserProfileView.as_view(), name='edit-profile'),
    path('profile/delete/', DeleteProfileView.as_view(), name='delete-profile'),
    path('profile/change-password/', CustomPasswordChangeView.as_view(), name='change-password'),
]