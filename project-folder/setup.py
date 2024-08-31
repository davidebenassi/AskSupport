import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AskSupport.settings')
django.setup()


from AskSupport.DBSetup import initDB, eraseDB


if __name__ == "__main__":
    eraseDB() 
    initDB()
    