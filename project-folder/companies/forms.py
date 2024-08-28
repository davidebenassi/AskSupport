from django import forms
from django.contrib.auth.models import Group
#from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from .models import Company

from users.forms import UserForm 

'''
class CompanyAdminForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
'''

class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ['name', 'description']

# * Rendered Form to register a new Company and its Admin * #
class CompanySignupForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.admin_form = CompanyAdminForm(*args, **kwargs)
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
