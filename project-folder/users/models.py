from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='related_profile')
    
    profilePicture = models.ImageField(
        upload_to='static/images/users_profile_pictures/',
        default='static/images/default/blank_profile_picture.jpg',
        blank=True      # Optional field 
    )

    def __str__(self):
      return f'{self.user.first_name} {self.user.last_name} - {self.user.username}'
