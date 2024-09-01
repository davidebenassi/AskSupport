from django.shortcuts import render
from django.contrib.auth.views import LoginView

def home(request):
    return render(request, 'home.html')

def signup_page(request):
    return render(request, 'signup_page.html')

class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        # Check if user is in "CompanyAdministrators" group
        if user.groups.filter(name='CompanyAdministrators').exists():
            return '/companies/admin-dashboard/'  # Reindirizza alla dashboard dell'admin
        # Check if user is in another group, e.g., "Employees"
        elif user.groups.filter(name='Employees').exists():
            return '/companies/employee-dashboard/'  # Reindirizza alla dashboard degli impiegati
        else:
            return '/'  # Default redirect