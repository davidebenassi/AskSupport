from companies.models import Company, EmployeeProfile
from tickets.models import Ticket, Message
from users.models import UserProfile
from django.contrib.auth.models import User
from AskSupport.settings import STATICFILES_DIRS
import os

ADMIN_USERNAME = 'admin'
ADMIN_PWD = 'admin'

def eraseDB():
    print("Erasing DataBase")
    
    Message.objects.all().delete()
    Ticket.objects.all().delete()
    EmployeeProfile.objects.all().delete()
    Company.objects.all().delete()
    UserProfile.objects.all().delete()
    User.objects.all().delete()

    
    profilePicturesFolders = [
        'images/users_profile_pics',
        'images/employees_profile_pics'
    ]

    staticFolderPath = os.path.abspath(STATICFILES_DIRS[0])

    for folder in profilePicturesFolders:
        absPath = os.path.join(staticFolderPath, folder)
        
        if not os.path.exists(absPath):
            os.makedirs(absPath)
        
        if os.path.exists(absPath):
            for f in os.listdir(absPath):
                filePath = os.path.join(absPath, f)
                if os.path.isfile(filePath):
                    os.remove(filePath)

    print("DataBase and images Erased.")

def initDB():
    admin = User.objects.create_superuser(username=ADMIN_USERNAME, password=ADMIN_PWD)
    admin.save
    print(f"Superuser Created with username : {ADMIN_USERNAME}  -  password : {ADMIN_PWD}")