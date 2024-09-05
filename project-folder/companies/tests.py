from django.test import TestCase
from AskSupport import settings
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from companies.models import Company, FAQ, EmployeeProfile
from django.test import Client

class FAQTests(TestCase):

    def setUp(self):
        # Creazione di un utente amministratore
        self.admin_user = User.objects.create_user(username='admin', password='adminpassword')
        admin_group = Group.objects.create(name='CompanyAdministrators')
        self.admin_user.groups.add(admin_group)

        # Creazione di un'azienda
        self.company = Company.objects.create(name='Test Company', description='A test company', admin=self.admin_user)

        # Creazione di alcune FAQ
        self.faq1 = FAQ.objects.create(question="What is this?", answer="This is a test FAQ.", company=self.company, approved=True)
        self.faq2 = FAQ.objects.create(question="How does it work?", answer="It works with magic.", company=self.company, approved=True)
        self.faq3 = FAQ.objects.create(question="Can I trust this?", answer="Of course!", company=self.company, approved=False)

        # Client per simulare le richieste
        self.client = Client()

    def test_faq_rendering(self):
        url = reverse('company-page', args=[self.company.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'company_page.html')
        self.assertContains(response, self.faq1.question)
        self.assertContains(response, self.faq2.answer)
        self.assertNotContains(response, self.faq3.question)  # FAQ non approvata non dovrebbe essere visibile

    def test_faq_search_functionality(self):
        # test funzionalità di ricerca delle FAQ
        url = reverse('company-page', args=[self.company.id])
        response = self.client.get(url, {'q': 'work'})  # Cerco la parola "work"
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.faq2.question)  # La FAQ con "work" nella domanda dovrebbe apparire

    def test_create_faq_by_employee(self):
        # creo un dipendente e test creazione di una FAQ
        employee_user = User.objects.create_user(username='employee', password='employeepassword')
        employee_group = Group.objects.create(name='Employees')
        employee_user.groups.add(employee_group)

        employee_profile = EmployeeProfile()
        employee_profile.user = employee_user
        employee_profile.company = self.company
        employee_profile.save()

        self.client.login(username='employee', password='employeepassword')

        response = self.client.post(reverse('employee-dashboard'), {
            'question': 'New FAQ question?',
            'answer': 'New FAQ answer.',
        })

        # La FAQ creata ma non approvata
        self.assertEqual(FAQ.objects.count(), 4)
        new_faq = FAQ.objects.last()
        self.assertEqual(new_faq.question, 'New FAQ question?')
        self.assertFalse(new_faq.approved)  

    def test_faq_approval_by_admin(self):
        # test approvazione di una FAQ da parte dell'amministratore
        self.client.login(username='admin', password='adminpassword')

        faq_to_approve = FAQ.objects.create(question="Is this pending?", answer="Yes.", company=self.company, approved=False)
        url = reverse('approve-faq', args=[faq_to_approve.id])

        response = self.client.post(url)

        # verifica approvazione FAQ
        faq_to_approve.refresh_from_db()
        self.assertTrue(faq_to_approve.approved)
    
    def test_faq_approval_by_guest(self):
        # test approvazione FAQ da parte di un utente non registrato

        faq_to_approve = FAQ.objects.create(question="Is this pending?", answer="Yes.", company=self.company, approved=False)
        url = reverse('approve-faq', args=[faq_to_approve.id])

        response = self.client.post(url)

        faq_to_approve.refresh_from_db()
        # Controllo il redirect alla pagina di login 
        self.assertRedirects(response, f'{settings.LOGIN_URL}&next={url}')

    def test_faq_deletion_by_admin(self):
        # test eliminazione di una FAQ da parte dell'amministratore
        self.client.login(username='admin', password='adminpassword')

        url = reverse('delete-faq', args=[self.faq1.id])
        response = self.client.post(url)

        # verifica che la FAQ sia stata eliminata
        self.assertFalse(FAQ.objects.filter(id=self.faq1.id).exists())

