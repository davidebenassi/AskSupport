from django.urls import path
from . import views

urlpatterns = [
    #path('signup/', views.register_user, name='register_user'),
    path('signup/', views.UserSignupView.as_view(), name='user_signup'),
]