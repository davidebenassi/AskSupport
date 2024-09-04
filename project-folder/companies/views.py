from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import FormView, DetailView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.exceptions import PermissionDenied
from braces.views import GroupRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.contrib.auth import login, authenticate, logout
from django.views import View
from .models import Company, EmployeeProfile
from .forms import CompanySignupForm, EmployeeSignupForm, CompanyForm
from tickets.forms import TicketForm
from tickets.models import Ticket
from faq.models import FAQ
from users.forms import ConfirmPasswordForm, EditUserForm
from django.contrib.auth.views import PasswordChangeView
from faq.forms import FAQCreateForm

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
        company = self.get_object()
        context['faqs'] = company.faqs.all().filter(approved=True)
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
        return self.request.user.related_company

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = self.get_object()  
        employees = EmployeeProfile.objects.filter(company=company)
        context['employees'] = employees
        context['form'] = self.get_form() 

        # Aggiunta dei dati per il grafico a torta
        context['total_tickets'] = Ticket.objects.filter(company=company).count()
        context['pending_tickets'] = Ticket.objects.filter(company=company, status=Ticket.PENDING).count()
        context['open_tickets'] = Ticket.objects.filter(company=company, status=Ticket.OPEN).count()
        context['closed_tickets'] = Ticket.objects.filter(company=company, status=Ticket.CLOSED).count()

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['company'] = self.get_object()
        return kwargs

    def get_success_url(self):
        return reverse_lazy('admin-dashboard')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save() 
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

    company = employee_profile.company
    faqs = company.faqs.all()
    notApprovedFaqs = faqs.filter(approved=False)
    approvedFaqs = faqs.filter(approved=True)

    if request.method == 'POST':
        form = FAQCreateForm(request.POST)
        if form.is_valid():
            faq = form.save(commit=False)
            faq.company = company

            faq.approved = False
            faq.save()
            return redirect('employee-dashboard')
    else:
        form = FAQCreateForm()

    return render(request, 'employee_dashboard.html', context={
        'open_tickets' : companyTickets.filter(assigned_employee=employee_profile, status=Ticket.OPEN).order_by('-priority'),
        'pending_tickets' : companyTickets.filter(status=Ticket.PENDING).order_by('-priority'),
        'closed_tickets' : companyTickets.filter(assigned_employee=employee_profile, status=Ticket.CLOSED),
        'already_handled_tickets' : companyTickets.filter(status=Ticket.OPEN).exclude(assigned_employee=employee_profile),
        'form': form,
        'notApprovedFaqs': notApprovedFaqs,
        'approvedFaqs': approvedFaqs
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


# * --- COMPANY UPDATE --- * #
class CompanyAdminPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_url = reverse_lazy('company-profile')

class CompanyProfileView(DetailView):
    model = Company
    template_name = 'company_profile.html'

    def get_object(self):
        return self.request.user.related_company
    

class DeleteCompanyView(FormView):
    template_name = 'delete_confirmation.html'
    form_class = ConfirmPasswordForm
    success_url = reverse_lazy('home')  

    def form_valid(self, form):
        password = form.cleaned_data['password']
        admin = authenticate(username=self.request.user.username, password=password)

        if admin is not None:
            admin.delete() 
            logout(self.request)  
            return super().form_valid(form)
        else:
            form.add_error('password', 'Incorrect password.')
            return self.form_invalid(form)
        
class UpdateCompanyProfileView(View):
    template_name = 'update_company_profile.html'
    success_url = reverse_lazy('company-profile')

    def get(self, request, *args, **kwargs):
        admin_form = EditUserForm(instance=request.user)
        company_form = CompanyForm(instance=request.user.related_company)

        return render(request, self.template_name, {
            'admin_form': admin_form,
            'company_form': company_form,
        })

    def post(self, request, *args, **kwargs):
        admin_form = EditUserForm(request.POST, instance=request.user)
        company_form = CompanyForm(request.POST, request.FILES, instance=request.user.related_company)

        if admin_form.is_valid():
            admin_form.save()

        if company_form.is_valid():
            company_form.save()

        return redirect(self.success_url)
    
# * --- FAQ --- * #

@user_passes_test(is_admin)
def delete_faq(request, faq_id):
    faq = get_object_or_404(FAQ, id=faq_id, company=request.user.related_company)

    if request.method == "POST":
        faq.delete()
        return redirect('company-faq')

    return redirect('company-faq')

@user_passes_test(is_admin)
def approve_faq(request, faq_id):
    faq = get_object_or_404(FAQ, id=faq_id, company=request.user.related_company)

    if request.method == "POST":
        faq.approved = True
        faq.save()
        return redirect('company-faq')

    return redirect('company-faq')

@user_passes_test(is_admin)
def company_faq_view(request):
    company = request.user.related_company
    faqs = company.faqs.all()
    notApprovedFaqs = faqs.filter(approved=False)
    approvedFaqs = faqs.filter(approved=True)

    if request.method == 'POST':
        form = FAQCreateForm(request.POST)
        if form.is_valid():
            faq = form.save(commit=False)
            faq.company = company
            faq.approved = True  
            faq.save()
            return redirect('company-faq')
    else:
        form = FAQCreateForm()

    return render(request, 'company_faq.html', {'company': company, 'notApprovedFaqs': notApprovedFaqs, 'approvedFaqs' : approvedFaqs, 'form': form})