from django.urls import path
from . import views

urlpatterns = [
    path('', views.companies_home_page, name='companies_home_page'),
    path('<int:pk>/', views.company_page, name='company-page'),
    path('company-signup/', views.CompanySignupView.as_view(), name='company_signup'),
    
    path('employee-signup/', views.EmployeeSignupView.as_view(), name='employee_signup'),

    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('approve-employee/<int:employee_id>/', views.approve_employee, name='approve_employee'),
    path('remove-employee/<int:employee_id>/', views.remove_employee, name='remove_employee'),
    
    path('employee-dashboard/', views.employee_dashboard, name='employee-dashboard')
]

