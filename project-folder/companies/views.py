from django.shortcuts import render
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Company
from .forms import CompanySignupForm, EmployeeSignupForm


def is_admin(user):
    return user.groups.filter(name='CompanyAdministrators').exists()

def is_employee(user):
    return user.groups.filter(name='Employees').exists()



def companies_home_page(request):
    companies = Company.objects.all()
    return render(request, 'companies_home_page.html', {'companies': companies})

@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

@user_passes_test(is_employee)
def employee_dashboard(request):
    return render(request, 'employee_dashboard.html')

# Using FormView instead of CreateView to handle the compbinated CompanySignupForm (it contains 2 forms) #
class CompanySignupView(FormView):
    form_class = CompanySignupForm
    template_name = 'company_signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()  # Save data using CompanySignupForm.save()
        return super().form_valid(form)

class EmployeeSignupView(FormView):
    form_class = EmployeeSignupForm
    template_name = 'employee_signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()  
        return super().form_valid(form)