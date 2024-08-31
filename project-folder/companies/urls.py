from django.urls import path
from .views import *

urlpatterns = [
    path('', companies_home_page, name='companies_home_page'),
    path('<int:pk>/', company_page, name='company-page'),
    path('company-signup/', CompanySignupView.as_view(), name='company_signup'),
    
    #path('employee-signup/', views.EmployeeSignupView.as_view(), name='employee_signup'),

    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('approve-employee/<int:employee_id>/', approve_employee, name='approve_employee'),
    path('remove-employee/<int:employee_id>/', remove_employee, name='remove_employee'),
    
    path('employee-dashboard/', employee_dashboard, name='employee-dashboard')
]

