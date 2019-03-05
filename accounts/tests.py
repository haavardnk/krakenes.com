import json
from django.test import TransactionTestCase
from django.contrib.auth.models import User
from django.contrib import auth

# Create your tests here.


class BaseTestCase(TransactionTestCase):
    '''
    Basic test setup for authorization
    '''

    def setUp(self):
        user = User.objects.create_user(
            username='testuser', email='test@test.com', password='testpass')


class LoginTests(BaseTestCase):

    def test_login_success(self):
        response = self.client.post("/accounts/login", {"username": "testuser", "password": "testpass", "next": "/"}, **{
                                    'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(json.loads(response.content)['login'], "success")

    def test_login_wrong_password(self):
        response = self.client.post("/accounts/login", {"username": "testuser", "password": "wrongpassword", "next": "/"}, **{
                                    'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(json.loads(response.content)['login'], "password")

    def test_login_wrong_username(self):
        response = self.client.post("/accounts/login", {"username": "wronguser", "password": "wrongpassword", "next": "/"}, **{
                                    'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(json.loads(response.content)['login'], "nouser")

    def test_login_not_post(self):
        response = self.client.get("/accounts/login", {"username": "wronguser", "password": "wrongpassword", "next": "/"}, **{
            'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(json.loads(response.content)['login'], "failed")


class SignupTests(BaseTestCase):

    def test_signup_success(self):
        response = self.client.post("/accounts/signup", {"username": "testuser2", "password1": "testpass",
                                                         "password2": "testpass", "email": "test@email.com", "next": "/"}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(json.loads(response.content)['register'], "success")

    def test_signup_username_taken(self):
        response = self.client.post("/accounts/signup", {"username": "testuser", "password1": "testpass",
                                                         "password2": "testpass", "email": "test@email.com", "next": "/"}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(json.loads(response.content)['register'], "user")

    def test_signup_email_taken(self):
        response = self.client.post("/accounts/signup", {"username": "testuser3", "password1": "testpass",
                                                         "password2": "testpass", "email": "test@test.com", "next": "/"}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(json.loads(response.content)['register'], "email")

    def test_signup_passwords_not_equal(self):
        response = self.client.post("/accounts/signup", {"username": "testuser3", "password1": "testpass",
                                                         "password2": "passtest", "email": "test@pass.com", "next": "/"}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(json.loads(response.content)['register'], "password")

    def test_signup_not_post(self):
        response = self.client.get("/accounts/signup", {"username": "testuser3", "password1": "testpass",
                                                        "password2": "passtest", "email": "test@pass.com", "next": "/"}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(json.loads(response.content)['register'], "failed")


class LogoutTests(BaseTestCase):

    def test_logout_success(self):
        self.client.login(username='testuser', password="testpass")
        response = self.client.post("/accounts/logout")
        self.assertEqual(response.status_code, 301)

    def test_logout_not_logged_in(self):
        response = self.client.post("/accounts/logout")
        self.assertEqual(response.status_code, 302)

class ProfileModelTests(BaseTestCase):
    
    def test_profile_model_str(self):
        user = User.objects.get(username='testuser')
        self.assertEqual(str(user.profile), user.username)