from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Company

class CompanyRegisterForm(forms.ModelForm):
    admin_username = forms.CharField(max_length=100)
    admin_password = forms.CharField(widget=forms.PasswordInput)
    admin_email = forms.EmailField()

    class Meta:
        model = Company
        fields = ['name', 'description']

    def save(self, commit=True):
        company = super().save(commit=False)
        admin_user = User.objects.create_user(
            username=self.cleaned_data['admin_username'],
            password=self.cleaned_data['admin_password'],
            email=self.cleaned_data['admin_email']
        )
        company.admin = admin_user
        if commit:
            company.save()
        return company
