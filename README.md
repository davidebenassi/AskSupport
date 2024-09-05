# AskSupport
A WebSite written in Django to allow users to request support from different companies.
Developed for the UNIMORE University Exam of Web Technologies.

# Follow these steps to run the website on your machine

## 0. Prerequisite - Install pipenv
Make sure pipenv is installed on your machine.
If it's not installed you can do it with
```bash
pip install [--user] pipenv
```

## 1. Cloning
```bash
git clone https://github.com/davidebenassi/AskSupport.git
cd AskSupport
```
## 2. Virual Environment

Open virtual-environment shell with:

```bash
pipenv install
pipenv shell
```
## 3. Install the Project requirements
Install all project dependencies listed in the requirements.txt file:
```bash
pip install -r requirements.txt
```
## 4. Configure the database
Move to the **project-folder**:
```bash
cd project-folder
```
Run the migrations to set up the database:
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```
## 5. Populate DB:
Run the following script to populate the DataBase with some start-up data:
```bash
python3 setup.py
```

## 6. Start the Django server:
```bash
python3 manage.py runserver
```
## 7. Usage
Once the server is running, you can access the online platform at http://localhost:8000/ 

### Startup Users

| Username    | Password                | User Type      |
|-------------|-------------------------|----------------|
| admin       | admin                   | Admin          |
| dbenassi, lrossi, gverdi, mbianchi | PSicura1! | User  |
| emp_smarconi, emp_rleone, emp_ericci, emp_fgalli, emp_cmonti | PSicura1! | Employee |
| adminarossi, adminlferrari, admingesposito, adminmromano | PSicura1! | Company Admin |
