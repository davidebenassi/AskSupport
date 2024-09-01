from django.urls import path
from .views import *

urlpatterns = [
    path('<int:pk>/', company_page, name='company-page'),
    path('company-signup/', CompanySignupView.as_view(), name='company_signup'),
    

    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('remove-employee/<int:employee_id>/', remove_employee, name='remove_employee'),
    
    path('employee-dashboard/', employee_dashboard, name='employee-dashboard')
]

