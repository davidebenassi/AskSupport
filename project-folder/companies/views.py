from django.shortcuts import render
from django.views.generic import FormView
from django.urls import reverse_lazy


from .models import Company
from .forms import CompanySignupForm

def companies_home_page(request):
    companies = Company.objects.all()
    return render(request, 'companies_home_page.html', {'companies': companies})

# Using FormView instead of CreateView to handle the compbinated CompanySignupForm (it contains 2 forms) #
class CompanySignupView(FormView):
    form_class = CompanySignupForm
    template_name = 'company_signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()  # Save data using CompanySignupForm.save()
        return super().form_valid(form)
