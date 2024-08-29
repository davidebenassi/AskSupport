from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description']
        
        widgets = {
            'title': forms.TextInput(),
            'description': forms.Textarea(),
        }


'''
'title': forms.TextInput(attrs={'class': 'form-control'}),
'description': forms.Textarea(attrs={'class': 'form-control'}),
'''