from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from braces.views import GroupRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django.contrib.auth import login

from .models import Company, EmployeeProfile
from .forms import CompanySignupForm, EmployeeSignupForm
from tickets.forms import TicketForm
from tickets.models import Ticket

def is_admin(user):
    return user.groups.filter(name='CompanyAdministrators').exists()

def is_employee(user):
    return user.groups.filter(name='Employees').exists()


# * --- COMPANIES & ADMIN --- * #

def companies_home_page(request):
    companies = Company.objects.all()
    return render(request, 'companies_home_page.html', {'companies': companies})

class CompanyPageView(FormMixin, DetailView):
    model = Company
    template_name = 'company_page.html'
    context_object_name = 'company'
    form_class = TicketForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def get_success_url(self):
        return reverse('company-page', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        ticket = form.save(commit=False)
        ticket.created_by = self.request.user.related_profile
        ticket.company = self.object
        ticket.save()
        return super().form_valid(form)
    
class AdminDashboardView(GroupRequiredMixin, FormMixin, DetailView):
    group_required = ['CompanyAdministrators']
    model = Company
    template_name = 'admin_dashboard.html'
    context_object_name = 'company'
    form_class = EmployeeSignupForm

    def get_object(self):
        # Restituisci l'azienda associata all'utente corrente
        return self.request.user.related_company

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = self.get_object()  # Recupera l'oggetto Company
        employees = EmployeeProfile.objects.filter(company=company)
        context['employees'] = employees
        context['form'] = self.get_form()  # Aggiungi il form al contesto
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['company'] = self.get_object()  # Passa l'azienda al form
        return kwargs

    def get_success_url(self):
        return reverse_lazy('admin-dashboard')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Imposta l'oggetto Company
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()  # Salva i dati dell'employee
        return super().form_valid(form)

@user_passes_test(is_admin)
def remove_employee(request, employee_id):
    employee = get_object_or_404(EmployeeProfile, id=employee_id)

    if employee.company.admin != request.user:
        raise PermissionDenied("You don't have permissions to remove this employee.")

    employee.user.delete()    
    employee.delete()

    return redirect(reverse('admin-dashboard'))


# * --- EMPLOYEES --- * #

@user_passes_test(is_employee)
def employee_dashboard(request):
    employee_profile = request.user.employee_profile
    companyTickets = Ticket.objects.filter(company=employee_profile.company)

    return render(request, 'employee_dashboard.html', context={
        'open_tickets' : companyTickets.filter(assigned_employee=employee_profile, status=Ticket.OPEN).order_by('-priority'),
        'pending_tickets' : companyTickets.filter(status=Ticket.PENDING).order_by('-priority'),
        'closed_tickets' : companyTickets.filter(assigned_employee=employee_profile, status=Ticket.CLOSED),
        'already_handled_tickets' : companyTickets.filter(status=Ticket.OPEN).exclude(assigned_employee=employee_profile)
        }
    )


# * --- FORM VIEWS --- * #
# Using FormView instead of CreateView to handle the compbinated CompanySignupForm (it contains 2 forms) #
class CompanySignupView(FormView):
    form_class = CompanySignupForm
    template_name = 'company_signup.html'
    success_url = reverse_lazy('admin-dashboard')

    def form_valid(self, form):
        admin, _ = form.save()
        login(self.request, admin)
        return super().form_valid(form)
