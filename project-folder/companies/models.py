from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    admin = models.OneToOneField(User, on_delete=models.CASCADE, related_name='related_company')

    companyLogo = models.ImageField(
        upload_to='images/companies_logos/',
        default='images/default/blank_company_logo.png',
        blank=True      # Optional field 
    )


    def __str__(self):
        return self.name

class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.user.username} ({self.company.name})'
    
        
