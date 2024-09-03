from django.db import models
from companies.models import Company

class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='faqs')
    approved = models.BooleanField(default=False)