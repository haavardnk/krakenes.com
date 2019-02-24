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

class TestSignupPage(BaseTestCase):
    '''
    Tests of the signup page
    '''
    def test_signup_page_status_code(self):
        response = self.client.get('/accounts/signup')
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('signup'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')

    def test_signup_page_contains_correct_html(self):
        response = self.client.get('/accounts/signup')
        self.assertContains(response, '<h1 class="display-5">Sign Up!</h1>')

    def test_signup_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/accounts/signup')
        self.assertNotContains(
            response, 'Not in signup')

    def test_signup_page_contains_form(self):
        response = self.client.get('/accounts/signup')
        self.assertContains(response, 'Username')
        self.assertContains(response, 'First Name')
        self.assertContains(response, 'Last Name')
        self.assertContains(response, 'email@example.com')
        self.assertContains(response, 'Password')
        self.assertContains(response, 'Confirm Password')
        self.assertContains(response, 'btn btn-lg btn-block btn-success')
    
    def test_signup_passwords_not_matching(self):
        response = self.client.post('/accounts/signup', {
            'username':'testsignup',
            'first_name':'test',
            'last_name':'user',
            'email':'test@email.com',
            'password1':'testpass',
            'password2':'passtest'
            })
        self.assertTemplateUsed(response, 'accounts/signup.html')
        self.assertContains(response, 'Passwords must match')

    def test_signup_success(self):
        response = self.client.post('/accounts/signup', {
            'username':'testsignup',
            'first_name':'test',
            'last_name':'user',
            'email':'test@email.com',
            'password1':'testpass',
            'password2':'testpass'
            }, follow=True)
        self.assertTemplateUsed(response, 'blog/home.html')
        self.assertTrue(response, User.is_authenticated)
        self.assertTrue(response, User.objects.get(username='testsignup'))