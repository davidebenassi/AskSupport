from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import UserProfile

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        labels = {
            'first_name' : 'Name',
            'last_name' : 'Surname',
            'email' : 'e-mail address'
        }

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['profilePicture']
        labels = {
            'profilePicture' : 'Profile Picture'
        }
        widgets = {
            'profilePicture' : forms.FileInput(attrs={'class': 'form-control'})
        }

# * Update Profile * #
class EditUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
    
    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.fields.pop('password', None)


class ConfirmPasswordForm(forms.Form):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Enter your password to confirm deletion."
    )

# * Rendered Form to register a new User * #
class UserSignupForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.userForm = UserForm(*args, **kwargs)
        self.userProfileForm = UserProfileForm(*args, **kwargs)
    
    def is_valid(self) -> bool:
        return self.userForm.is_valid() and self.userProfileForm.is_valid()
    
    def save(self, commit=True):
        user = self.userForm.save(commit=False)
        if commit:
            user.save()

        profile = self.userProfileForm.save(commit=False)
        profile.user = user
        if commit:
            profile.save()

        return user, profile        

