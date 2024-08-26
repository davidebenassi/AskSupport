from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.UserSignupView.as_view(), name='user_signup'),
]