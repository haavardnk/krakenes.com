from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
# Create your tests here.
class BaseTestCase(TestCase):
    '''
    Basic test setup for accounts testing
    ''' 
    def setUp(self):
        user = User.objects.create_user(username='testuser2', email='test@test.com', password='testpass2')

class TestLoginPage(BaseTestCase):
    '''
    Tests of the login page
    '''
    def test_login_page_status_code(self):
        response = self.client.get('/accounts/login')
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_page_contains_correct_html(self):
        response = self.client.get('/accounts/login')
        self.assertContains(response, '<h1 class="display-5">Login</h1>')

    def test_login_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/accounts/login')
        self.assertNotContains(
            response, 'Not in login')

    def test_login_page_contains_form(self):
        response = self.client.get('/accounts/login')
        self.assertContains(response, 'Username')
        self.assertContains(response, 'Password')
        self.assertContains(response, 'btn btn-lg btn-block btn-success')
