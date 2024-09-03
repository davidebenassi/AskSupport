from companies.models import Company, EmployeeProfile
from tickets.models import Ticket, Message
from users.models import UserProfile
from django.contrib.auth.models import User, Group
from AskSupport.settings import STATICFILES_DIRS
import os
import json
from django.db import transaction, connection

ADMIN_USERNAME = "admin"
ADMIN_PWD = "admin"

def reset_ids(tables):
	for t in tables:
		with connection.cursor() as cursor:
			cursor.execute(f"DELETE FROM sqlite_sequence WHERE name = '{t}';")

def eraseDB():
    print("Erasing DataBase")
    
    Message.objects.all().delete()
    Ticket.objects.all().delete()
    EmployeeProfile.objects.all().delete()
    Company.objects.all().delete()
    UserProfile.objects.all().delete()
    User.objects.all().delete()

    
    profilePicturesFolders = [
        'images/users_profile_pictures',
        'images/employees_profile_pictures'
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
    admin.save()
    print(f"Superuser Created with username : {ADMIN_USERNAME}  -  password : {ADMIN_PWD}")

    # Creazione Utenti #
    usersJsonFile = os.path.join(os.path.dirname(__file__), 'DBSetupJson', 'users.json')
    with open(usersJsonFile, 'r') as file:
        data = json.load(file)

    for item in data:
        user = User.objects.create_user(
            username = item['username'],
            password = item['password'],
            email = item['email'],
            first_name = item['first_name'],
            last_name = item['last_name']
        )
        user.save()

        userProfile = UserProfile()
        userProfile.user = user
        userProfile.save()

    ## Crea azienda 1 #
    # Admin
    admin = User.objects.create_user(
            username = 'adminazienda',
            password = 'PSicura1!',
            email = 'admin@azienda.it',
            first_name = 'Luca',
            last_name = 'Valori'
        )
    Group.objects.get(name='CompanyAdministrators').user_set.add(admin)
    admin.save()
    # Company
    c = Company()
    c.name = 'Azienda 1'
    c.description = "Azienda tech"
    c.admin = admin
    c.save()


        
