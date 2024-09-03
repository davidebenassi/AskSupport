from django.shortcuts import render
from django.contrib.auth.views import LoginView

def home(request):
    return render(request, 'home.html')

def signup_page(request):
    return render(request, 'signup_page.html')

class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.groups.filter(name='CompanyAdministrators').exists():
            return '/companies/admin-dashboard/' 
        elif user.groups.filter(name='Employees').exists():
            return '/companies/employee-dashboard/' 
        else:
            return '/' 