from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.core.exceptions import PermissionDenied

from .models import Company, EmployeeProfile
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
    company = request.user.related_company
    unapproved_employees = EmployeeProfile.objects.filter(company=company, is_approved=False)
    approved_employees = EmployeeProfile.objects.filter(company=company, is_approved=True)
    
    context = {
        'unapproved_employees': unapproved_employees,
        'approved_employees': approved_employees,
    }
    return render(request, 'admin_dashboard.html', context)

@user_passes_test(is_employee)
def employee_dashboard(request):
    return render(request, 'employee_dashboard.html')

@user_passes_test(is_admin)
def approve_employee(request, employee_id):
    employee = get_object_or_404(EmployeeProfile, id=employee_id)

     # Verifica che l'admin sia l'admin della stessa Company
    if employee.company.admin != request.user:
        raise PermissionDenied("Non hai i permessi per approvare questo dipendente.")
    
    employee.is_approved = True
    employee.save()

    return redirect(reverse('admin-dashboard?login=ok'))

@user_passes_test(is_admin)
def remove_employee(request, employee_id):
    employee = get_object_or_404(EmployeeProfile, id=employee_id)

    if employee.company.admin != request.user:
        raise PermissionDenied("Non hai i permessi per approvare questo dipendente.")
        
    employee.is_approved = False
    employee.company = None
    employee.save()

    return redirect(reverse('admin-dashboard?login=ok'))



# * --- Form Views --- * #
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