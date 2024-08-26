from django.urls import path
from . import views

urlpatterns = [
    path('', views.companies_home_page, name='companies_home_page'),
    path('signup/', views.CompanySignupView.as_view(), name='company_signup'),

]

