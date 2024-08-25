from django.shortcuts import render, redirect
from .models import Company
from .forms import CompanyRegisterForm

def companies_home_page(request):
    companies = Company.objects.all()
    return render(request, 'companies_home_page.html', {'companies': companies})

def register_company(request):
    if request.method == 'POST':
        form = CompanyRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('companies_home_page')
    else:
        form = CompanyRegisterForm()
    return render(request, 'register_company.html', {'form': form})
