# AskSupport
A WebSite written in Django to allow users to request support from different companies.
Developed for the UNIMORE University Exam of Web Technologies.

## Users
*Superuser Login*: admin admin 

<!-- 

# Install

After making sure `pipenv` is installed, create the virtual env on the top level of the folder
```
pipenv shell
```
Dependencies contained in `requirements.txt`should be installed automatically. 
However, they can be installed manually by:
```
pipenv install -r requirements.txt
```
# Problems due to the version of the libraries needed
There may be problems with the versions present in the requirements. In that case install libraries manually by creating the virtual env: 
```
pipenv shell
```
then
```
pipenv install django
pipenv install pillow
pipenv install django-widget-tweaks
```
# Database
Enter inside the project directory by
```
cd FieldHub/
```
so you should be in `~/FieldHub/FieldHub`.
Setup the database by 
```
python manage.py makemigrations
python manage.py migrate
```
After being moved into `FieldHub/` launch:
```
python setup.py
```
This will initially populate database. 

# Startup
Start the Django server:
```
python manage.py runserver
```
You can access to the website through `http://localhost:8000/`.

Using **google chrome** is recommended.

# Users already available
Initial users correspond to te one defined inside the directory `FieldHub/FieldHub/initDBJson` and they are
| Username    | Password                | Tipo di Utente |
|-------------|-------------------------|----------------|
| admin       | passwordadmin           | Admin          |
| Alberto     | passwordutente          | Utente         |
| Chiara      | passwordutente          | Utente         |
| Marco       | passwordutente          | Utente         |
| Giulia      | passwordutente          | Utente         |
| Luca        | passwordutente          | Utente         |
| Matteo123   | passwordutente          | Utente         |
| Sara456     | passwordutente          | Utente         |
| Marco789    | passwordutente          | Utente         |
| Elena321    | passwordutente          | Utente         |
| Davide654   | passwordutente          | Utente         |
| Alice987    | passwordutente          | Utente         |
| Francesco543| passwordutente          | Utente         |
| Chiara678   | passwordutente          | Utente         |
| Giorgio345  | passwordutente          | Utente         |
| Martina210  | passwordutente          | Utente         |
| Federico09  | passwordstruttura       | Struttura      |
| Mario10     | passwordstruttura       | Struttura      |
| Luca11      | passwordstruttura       | Struttura      |
| Giorgio12   | passwordstruttura       | Struttura      |
| Andrea13    | passwordstruttura       | Struttura      |
| Chiara14    | passwordstruttura       | Struttura      |
| Davide15    | passwordstruttura       | Struttura      |
| Elena16     | passwordstruttura       | Struttura      |
| Francesco17 | passwordstruttura       | Struttura      |
| Giulia18    | passwordstruttura       | Struttura      |
| Laura19     | passwordstruttura       | Struttura      |
| Marco20     | passwordstruttura       | Struttura      |
| Simone21    | passwordstruttura       | Struttura      |
| Valentina22 | passwordstruttura       | Struttura      |
| Alessandro23| passwordstruttura       | Struttura      |
| Martina24   | passwordstruttura       | Struttura      |

































# TennisCoach project

TechWeb Programmaing Project, based on Django.

This project aims to revolutionize tennis learning by creating a robust, scalable, and user-friendly platform for purchasing and accessing high-quality online courses

## Required Libraries

**django**==5.0.6; -> framework principale utilizzato per sviluppare l'applicazione web

**django-bootstrap5**==24.2; -> integra Bootstrap 5 con Django

**django-braces**==1.15.0 -> fornisce un insieme di mixins che facilitano l'implementazione di funzionalità comuni nelle viste class-based (CBV) di Django, come il controllo dell'appartenenza ad un gruppo.

**django-crispy-forms**==2.2; -> facilita la gestione dei form Django

**django-payments**==2.0.0; -> fornisce un'astrazione comune per gestire pagamenti online con diversi provider di pagamento

**moviepy**==1.0.3; -> libreria usata per gestire i video ed estrarne la lunghezza

**pillow**==10.4.0; -> libreria usata per l'elaborazione delle immagini

**stripe**==10.1.0; -> SDK ufficiale di Stripe per Python, utilizzata per interagire con l'API di Stripe e gestire pagamenti

## Setup

Follow these steps to set up and run the application:

### 1. Cloning
```bash
git clone https://github.com/StayLode/TennisCoach.git
cd TennisCoach
```
### 2. Install pipenv

Make sure pipenv is installed.
Locally install dependencies, then open virtual-environment shell with:

```bash
pipenv install
pipenv shell
```
### 3. Install the requirements
Install all project dependencies listed in the requirements.txt file:
```bash
pip install -r requirements.txt
```
### 4. Configure the database
Run the migrations to set up the database:
```bash
python manage.py makemigrations
python manage.py migrate
```
### 5. Populate DB:
Run the following file, which contains functions to setup a default environment with some users and courses
```bash
python setup.py
```

## Running
### 1. Start the Django server:
```bash
python manage.py runserver
```
### 2. Usage
Once the server is running, you can access the online tennis courses.
Go to http://localhost:8000/ and start exploring.

**Utenti di prova**

_USERNAME_ -> per tutti gli utenti
- _Customer_: matteo, lode, nicholas, andrea
- _Coach_: mezzanotte, prampolini, ugolini, menabue
- _Admin_: admin

_PASSWORD_ -> per tutti gli utenti
- 123

-->