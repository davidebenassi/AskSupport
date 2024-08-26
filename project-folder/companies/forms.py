from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Company

class CompanyAdminForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ['name', 'description']

'''
This form register an Admin and a company
'''
class CompanySignupForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.admin_form = CompanyAdminForm(*args, **kwargs)
        self.company_form = CompanyForm(*args, **kwargs)
        

    def is_valid(self):
        return self.admin_form.is_valid() and self.company_form.is_valid()

    def save(self, commit=True):
        # Salva l'utente admin
        user = self.admin_form.save(commit=False)
        if commit:
            user.save()

            # Aggiungi l'utente al gruppo "CompanyAdministrators"
            group, created = Group.objects.get_or_create(name='CompanyAdministrators')
            user.groups.add(group)

        # Salva l'azienda associando l'utente appena creato come admin
        company = self.company_form.save(commit=False)
        company.admin = user
        if commit:
            company.save()

        return user, company
