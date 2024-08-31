from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from braces.views import GroupRequiredMixin


from .models import Company, EmployeeProfile
from .forms import CompanySignupForm, EmployeeSignupForm


def is_admin(user):
    return user.groups.filter(name='CompanyAdministrators').exists()

def is_employee(user):
    return user.groups.filter(name='Employees').exists()




def companies_home_page(request):
    companies = Company.objects.all()
    return render(request, 'companies_home_page.html', {'companies': companies})

def company_page(request, pk):
    company = get_object_or_404(Company, pk=pk)
    return render(request, 'company_page.html', {'company': company})
    
class AdminDashboardView(GroupRequiredMixin, FormView):
    group_required = ["CompanyAdministrators"]
    form_class = EmployeeSignupForm
    template_name = 'admin_dashboard.html'
    success_url = reverse_lazy('admin-dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = self.request.user.related_company
        employees = EmployeeProfile.objects.filter(company=company)
        context['employees'] = employees
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['company'] = self.request.user.related_company  # Passa la company al form
        return kwargs

    def form_valid(self, form):
        form.save()  # Salva i dati dell'employee
        return super().form_valid(form)


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

'''
class EmployeeSignupView(FormView):
    form_class = EmployeeSignupForm
    template_name = 'employee_signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()  
        return super().form_valid(form)
'''