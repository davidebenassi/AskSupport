from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
   
    picture = models.ImageField(
        upload_to='static/users_profile_pictures/',
        default='static/images/blank_profile_picture.jpg',
        blank=True
    )
    #tickets = models.ManyToManyField(to = '', through = '', blank = True, related_name = 'userTickets')

    def __str__(self):
      return f'{self.user.first_name} {self.user.last_name} - {self.user.username}'
