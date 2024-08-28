from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    admin = models.OneToOneField(User, on_delete=models.CASCADE, related_name='related_company')

    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} ({self.company.name})'
