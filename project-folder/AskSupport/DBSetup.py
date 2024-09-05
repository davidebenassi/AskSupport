from companies.models import Company, EmployeeProfile, FAQ
from tickets.models import Ticket, Message
from users.models import UserProfile
from django.contrib.auth.models import User, Group
from AskSupport.settings import STATICFILES_DIRS
import os
import json
from django.db import connection
import random
from django.apps import apps

ADMIN_USERNAME = "admin"
ADMIN_PWD = "admin"

def reset_tables_ids(tables):
	for t in tables:
		with connection.cursor() as cursor:
			cursor.execute(f"DELETE FROM sqlite_sequence WHERE name = '{t}';")

def eraseDB():
    print("Erasing DataBase")
    
    FAQ.objects.all().delete()
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

    tables = ['auth_user', 'companies_company', 'companies_employeeprofile', 'companies_faq', 'users_userprofile', 'tickets_ticket', 'tickets_message', 'faq_faq']
    reset_tables_ids(tables)

    admin = User.objects.create_superuser(username=ADMIN_USERNAME, password=ADMIN_PWD)
    admin.save()
    print(f"Superuser Created with username : {ADMIN_USERNAME}  -  password : {ADMIN_PWD}")

    adminGroup, created = Group.objects.get_or_create(name='CompanyAdministrators')
    empGroup, created = Group.objects.get_or_create(name='Employees')

    ## * Creazione Utenti * ##
    jsonFile = os.path.join(os.path.dirname(__file__), 'DBSetupJson', 'users.json')
    with open(jsonFile, 'r') as file:
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

    ## * Creazione Aziende * ##
    jsonFile = os.path.join(os.path.dirname(__file__), 'DBSetupJson', 'companies.json')
    with open(jsonFile, 'r') as file:
        data = json.load(file)
    
    for item in data:
        admin = User.objects.create_user(
                username = item['admin']['username'],
                password = item['admin']['password'],
                email = item['admin']['email'],
                first_name = item['admin']['first_name'],
                last_name = item['admin']['last_name']
            )
        adminGroup.user_set.add(admin)
        admin.save()
        
        c = Company()
        c.name = item['company']['name']
        c.description = item['company']['description']
        c.admin = admin
        c.save()


    ## * Get saved companies * ##
    companies = list(Company.objects.all())

    ## * Creazione Employee * ##

    jsonFile = os.path.join(os.path.dirname(__file__), 'DBSetupJson', 'employees.json')
    with open(jsonFile, 'r') as file:
        data = json.load(file)

    for item in data:
        emp = User.objects.create_user(
                username = item['username'],
                password = item['password'],
                email = item['email'],
                first_name = item['first_name'],
                last_name = item['last_name']
            )
        
        empGroup.user_set.add(emp)
        emp.save()

        empProfile = EmployeeProfile()
        empProfile.user = emp
        empProfile.company = random.choice(companies[:3]) # Leave a company without employees #   
        empProfile.save()

    ## * Creazione FAQs * ##

    jsonFile = os.path.join(os.path.dirname(__file__), 'DBSetupJson', 'faqs.json')
    with open(jsonFile, 'r') as file:
        data = json.load(file)

    for item in data[:4]:
        faq = FAQ()
        faq.question = item['question']
        faq.answer = item['answer']
        faq.approved = item['approved']
        faq.company = companies[0] 
        faq.save()     

    for item in data[4:7]:
        faq = FAQ()
        faq.question = item['question']
        faq.answer = item['answer']
        faq.approved = item['approved']
        faq.company = companies[1] 
        faq.save()   

    for item in data[7:10]:
        faq = FAQ()
        faq.question = item['question']
        faq.answer = item['answer']
        faq.approved = item['approved']
        faq.company = companies[1] 
        faq.save() 

    print("DB Setup Completed")
    print()

    print('Users')
    for u in list(UserProfile.objects.all()):
        print('\t', u)

    print()
    print('Companies')
    for c in companies:
        print('\t',c)

    print()
    print('Employees')
    for e in list(EmployeeProfile.objects.all()):
        print('\t', e)

    print()
    print("Created 10 FAQs")