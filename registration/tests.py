from django.test import TestCase
from django.urls import reverse
from .models import User, Family, Adult, Child
from datetime import date

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager


class SignUpPageTestCase(TestCase):

    def setUp(self):
        self.users = User.objects.all()

    def test_signup_page_returns_200(self):
        response = self.client.get(reverse('registration:signup'))
        self.assertEqual(response.status_code, 200)

    def test_signup_post_create_user(self):
        form = {
            'username': 'Fake-User',
            'email': 'fake.user@foo.bar',
            'password1': 'F4K3u53r',
            'password2': 'F4K3u53r'
        }
        old_users = self.users.count()
        response = self.client.post(reverse('registration:signup'), form)
        new_users = self.users.count()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(new_users, old_users+1)


class RegFamilyPageTestCase(TestCase):

    def setUp(self):
        self.username = 'Fake-User'
        self.email = 'fake.user@foo.bar'
        self.password = 'F4K3u53r'
        self.user = User.objects.create_user(self.username, self.email,
                                             self.password)
        self.client.login(username=self.username, password=self.password)
        self.form = {
            'use_name': 'FAKE',
            'home_phone': '0123456789',
            'home_address': '1 avenue Thomas More 12345 UTOPIA',
            'plan': 'CAF',
            'beneficiary_name': 'FAKE',
            'beneficiary_number': '12345F',
            'insurance_name': 'No Problemo',
            'insurance_number': 'NP987654',
            'lastname': 'MABOULE',
            'address': '2 avenue Thomas More 12345 UTOPIA',
            'job_phone': '9876543210'
        }

    def test_regfamily_page_returns_200(self):
        response = self.client.get(reverse('registration:regfamily'))
        self.assertEqual(response.status_code, 200)

    def test_regfamily_post_create_family(self):
        families = Family.objects.all()
        old_families = families.count()
        response = self.client.post(reverse('registration:regfamily'),
                                    self.form)
        new_families = families.count()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(new_families, old_families+1)

    def test_regfamily_post_create_doctor(self):
        doctors = Adult.objects.all()
        old_doctors = doctors.count()
        self.client.post(reverse('registration:regfamily'), self.form)
        new_doctors = doctors.count()
        self.assertEqual(new_doctors, old_doctors+1)


class ManageAccountPageTestCase(TestCase):

    def setUp(self):
        self.username = 'Fake-User'
        self.email = 'fake.user@foo.bar'
        self.password = 'F4K3u53r'
        self.user = User.objects.create_user(self.username, self.email,
                                             self.password)
        self.client.login(username=self.username, password=self.password)

    def test_myaccount_page_redirect_if_no_family(self):
        response = self.client.get(reverse('registration:myaccount'))
        self.assertEqual(response.status_code, 302)

    def test_myaccount_page_returns_200(self):
        Family.objects.create(user=self.user)
        response = self.client.get(reverse('registration:myaccount'))
        self.assertEqual(response.status_code, 200)


class RegChildPageTestCase(TestCase):

    def setUp(self):
        self.username = 'Fake-User'
        self.email = 'fake.user@foo.bar'
        self.password = 'F4K3u53r'
        self.user = User.objects.create_user(self.username, self.email,
                                             self.password)
        self.client.login(username=self.username, password=self.password)
        self.family = Family.objects.create(user=self.user)

        self.form = {
            'go_alone': False,
            'activity': True,
            'image_rights': True,
        }

    def test_regchild_pages_returns_200(self):
        response = self.client.get(reverse('registration:regchild_step1'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('registration:regchild_step2'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('registration:regchild_step3'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('registration:regchild_step4'))
        self.assertEqual(response.status_code, 200)

    def test_regchild_post_create_child_and_legalguardians(self):
        session = self.client.session
        session['child'] = {
            'firstname': 'fake',
            'lastname': 'fake',
            'birth_date': '2015-01-01',
            'grade': 'Primaire',
            'school': 'fake',
            'info': 'fake'
        }
        session['lg1'] = {
            'firstname': 'fake',
            'lastname': 'fake',
            'family_situation': 'fake',
            'address': 'fake',
            'occupation': 'fake',
            'job_phone': '0123456789',
            'cell_phone': '0123456789',
            'email': 'fake@foo.bar'
        }
        session['lg2'] = {
            'firstname': 'fake2',
            'lastname': 'fake2',
            'family_situation': 'fake2',
            'address': 'fake2',
            'occupation': 'fake2',
            'job_phone': '9876543210',
            'cell_phone': '9876543210',
            'email': 'fake2@foo.bar'
        }
        session.save()
        legal_guardians = Adult.objects.all()
        old_legal_guardians = legal_guardians.count()

        childs = Child.objects.all()
        old_childs = childs.count()

        response = self.client.post(reverse('registration:regchild_step4'),
                                    self.form)

        new_legal_guardians = legal_guardians.count()
        new_childs = childs.count()

        self.assertEqual(new_childs, old_childs+1)
        self.assertEqual(new_legal_guardians, old_legal_guardians+2)
        self.assertEqual(response.status_code, 302)


class RegPersonPageTestCase(TestCase):

    def setUp(self):
        self.username = 'Fake-User'
        self.email = 'fake.user@foo.bar'
        self.password = 'F4K3u53r'
        self.user = User.objects.create_user(self.username, self.email,
                                             self.password)
        self.client.login(username=self.username, password=self.password)
        self.family = Family.objects.create(user=self.user)
        self.form = {
            'firstname': 'fake',
            'lastname': 'fake',
            'cell_phone': '0123456789',
            'relationship': 'fake'
        }

    def test_regperson_page_returns_200(self):
        response = self.client.get(reverse('registration:regperson'))
        self.assertEqual(response.status_code, 200)

    def test_regperson_post_create_person(self):
        persons = Adult.objects.all()
        old_persons = persons.count()
        self.client.post(reverse('registration:regperson'), self.form)
        new_persons = persons.count()
        self.assertEqual(new_persons, old_persons+1)


class DeleteThisTestCase(TestCase):

    def setUp(self):
        self.username = 'Fake-User'
        self.email = 'fake.user@foo.bar'
        self.password = 'F4K3u53r'
        self.user = User.objects.create_user(self.username, self.email,
                                             self.password)
        self.client.login(username=self.username, password=self.password)
        self.family = Family.objects.create(user=self.user)
        self.birth_date = date.fromisoformat('2012-01-01')
        self.child = Child.objects.create(family=self.family,
                                          birth_date=self.birth_date)
        self.person = Adult.objects.create()
        self.family.authorized_person.add(self.person)

    def test_deletethis_remove_child(self):
        old_children = Child.objects.filter(family=self.family).count()
        self.client.post(reverse('registration:delete_this'),
                         {'this_kind': 'child', 'this_id': self.child.id})
        new_children = Child.objects.filter(family=self.family).count()
        self.assertEqual(new_children, old_children - 1)

    def test_deletethis_remove_authorized_person(self):
        family_friends = Adult.objects.filter(family_friends=self.family.id)
        old_family_friends = family_friends.count()
        self.client.post(reverse('registration:delete_this'),
                         {'this_kind': 'adult', 'this_id': self.person.id})
        new_family_friends = family_friends.count()
        self.assertEqual(new_family_friends, old_family_friends - 1)

    def test_deletethis_raise_404_if_nochild(self):
        response = self.client.post(
            reverse('registration:delete_this'),
            {'this_kind': 'child', 'this_id': '0'}
        )
        self.assertEqual(response.status_code, 404)

    def test_deletethis_raise_404_if_noperson(self):
        response = self.client.post(
            reverse('registration:delete_this'),
            {'this_kind': 'adult', 'this_id': '0'}
        )
        self.assertEqual(response.status_code, 404)


class FunctionalTestCase(StaticLiveServerTestCase):

    def setUp(self):
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        self.driver = webdriver.Firefox(
            executable_path=GeckoDriverManager().install(),
            firefox_options=opts
        )
        self.wait = WebDriverWait(self.driver, 1000)
        self.addCleanup(self.driver.quit)

    def test_create_account(self):
        self.driver.get(self.live_server_url)
        self.assertIn('Hazel', self.driver.title)

        dropdown = self.driver.find_element_by_id('dropdown-button')
        ActionChains(self.driver).click(dropdown).perform()
        self.wait.until(lambda driver:
                        self.driver.find_element_by_id("create-account"))
        create_account = self.driver.find_element_by_id('create-account')
        ActionChains(self.driver).click(create_account).perform()
        self.wait.until(lambda driver:
                        self.driver.find_element_by_id("submit-account"))

        assert self.driver.current_url.endswith('/registration/signup')

        username = self.driver.find_element_by_id('id_username')
        email = self.driver.find_element_by_id('id_email')
        password1 = self.driver.find_element_by_id('id_password1')
        password2 = self.driver.find_element_by_id('id_password2')
        submit = self.driver.find_element_by_id('submit-account')

        username.send_keys('fake-user')
        email.send_keys('fake@foo.bar')
        password1.send_keys('13tm31n21')
        password2.send_keys('13tm31n21')
        submit.send_keys(Keys.RETURN)

        self.wait.until(lambda driver:
                        self.driver.find_element_by_id("info"))

        assert self.driver.current_url == '{}/'.format(self.live_server_url)
