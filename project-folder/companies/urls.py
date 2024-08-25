from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.register_company, name='register_company'),
    path('', views.companies_home_page, name='companies_home_page'),
]

