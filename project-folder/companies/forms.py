from django import forms
from django.contrib.auth.models import Group
from .models import Company, EmployeeProfile

from users.forms import UserForm 

class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ['name', 'description', 'companyLogo']
        labels = {
            'companyLogo' : 'Company Logo'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'companyLogo' : forms.FileInput(attrs={'class': 'form-control'})
        }
        
class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = []

# * Rendered Form to register a new Company and its Admin * #
class CompanySignupForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.adminForm = UserForm(*args, **kwargs)
        self.companyForm = CompanyForm(*args, **kwargs)
        

    def is_valid(self) -> bool:
        return self.adminForm.is_valid() and self.companyForm.is_valid()

    def save(self, commit=True):
        
        # First, save the admin #
        admin = self.adminForm.save(commit=False)
        if commit:
            admin.save()

            # Add admin to "CompanyAdministrators" group #
            group, created = Group.objects.get_or_create(name='CompanyAdministrators')
            admin.groups.add(group)

        # Last, save the company with the proper admin #
        company = self.companyForm.save(commit=False)
        company.admin = admin
        if commit:
            company.save()

        return admin, company

class EmployeeSignupForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)
        self.userForm = UserForm(*args, **kwargs)
        self.employeeProfileForm = EmployeeProfileForm(*args, **kwargs)
   
    
    def is_valid(self) -> bool:
        return self.userForm.is_valid() and self.employeeProfileForm.is_valid()

    def save(self, commit=True):
        
        # First, save the user #
        user = self.userForm.save(commit=False)
        if commit:
            user.save()

            # Add user to "Employees" group #
            group, created = Group.objects.get_or_create(name='Employees')
            user.groups.add(group)

        # Last, save the employee with the proper user #
        employeeProfile = self.employeeProfileForm.save(commit=False)
        employeeProfile.user = user
        employeeProfile.company = self.company
        if commit:
            employeeProfile.save()

        return user, employeeProfile