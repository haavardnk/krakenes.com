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
        '''
        Tests that the login page returns the right response
        '''
        response = self.client.get('/accounts/login')
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        '''
        Tests that the login page uses the right template
        '''
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_page_contains_form(self):
        '''
        Tests that the login page contains the correct forms
        '''
        response = self.client.get('/accounts/login')
        self.assertContains(response, 'Username')
        self.assertContains(response, 'Password')
        self.assertContains(response, 'btn btn-lg btn-block btn-success')
    
    def test_login_page_login_wrong_user_or_pass(self):
        response = self.client.post('/accounts/login', {'username':'testuser2', 'password':'wrongpass'})
        self.assertContains(response, 'Username or password is incorrect.')

    def test_login_page_login(self):
        response = self.client.post('/accounts/login', {'username':'testuser2', 'password':'testpass2'}, follow=True)
        self.assertTemplateUsed(response, 'blog/home.html')
        self.assertTrue(response, User.is_authenticated)
        self.assertEqual(response.context["user"].username, 'testuser2')

class TestSignupPage(BaseTestCase):
    '''
    Tests of the signup page
    '''
    def test_signup_page_status_code(self):
        '''
        Tests that the signup page returns the right response
        '''
        response = self.client.get('/accounts/signup')
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        '''
        Tests that the signup page uses the right template
        '''
        response = self.client.get(reverse('signup'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')

    def test_signup_page_contains_form(self):
        '''
        Tests that the signup page contains the correct forms
        '''
        response = self.client.get('/accounts/signup')
        self.assertContains(response, 'Username')
        self.assertContains(response, 'First Name')
        self.assertContains(response, 'Last Name')
        self.assertContains(response, 'email@example.com')
        self.assertContains(response, 'Password')
        self.assertContains(response, 'Confirm Password')
        self.assertContains(response, 'btn btn-lg btn-block btn-success')
    
    def test_signup_passwords_not_matching(self):
        '''
        Tests that user signup with non-matching passwords works as expected
        '''
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

    def test_signup_username_taken(self):
        '''
        Tests that user signup with username taken works as expected
        '''
        response = self.client.post('/accounts/signup', {
            'username':'testuser2',
            'first_name':'test',
            'last_name':'user',
            'email':'test@email.com',
            'password1':'testpass',
            'password2':'testpass'
            })
        self.assertTemplateUsed(response, 'accounts/signup.html')
        self.assertContains(response, 'Username has already been taken!')

    def test_signup_success(self):
        '''
        Tests that a successful user signup works as expected
        '''
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
        self.assertTrue(response.context["user"].username, 'testsignup')