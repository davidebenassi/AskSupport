from django.urls import path
from .views import *

urlpatterns = [
    path('<int:pk>/', CompanyPageView.as_view(), name='company-page'),
    path('company-signup/', CompanySignupView.as_view(), name='company-signup'),
    path('profile/', CompanyProfileView.as_view(), name='company-profile'),
    path('profile/edit/', UpdateCompanyProfileView.as_view(), name='edit-company'),
    path('profile/delete/', DeleteCompanyView.as_view(), name='delete-company'),
    path('profile/change-password/', CompanyAdminPasswordChangeView.as_view(), name='change-admin-password'),

    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('remove-employee/<int:employee_id>/', remove_employee, name='remove-employee'),
    
    path('employee-dashboard/', employee_dashboard, name='employee-dashboard')
]

