from django import forms
from .models import FAQ

class FAQCreateForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question', 'answer']
        labels = {
            'question' : 'Question',
            'answer' : 'Answer'
        }
        widgets = {
            'question': forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
            'answer': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }