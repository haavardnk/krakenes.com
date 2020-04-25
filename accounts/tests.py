import json
from django.test import TransactionTestCase
from django.contrib.auth.models import User


class BaseTestCase(TransactionTestCase):
    '''
    Basic test setup for authorization
    '''

    def setUp(self):
        user = User.objects.create_user(
            username='testuser', email='test@test.com', password='testpass')

class LogoutTests(BaseTestCase):
    '''
    Tests logging out
    '''

    def test_logout_success(self):
        self.client.login(username='testuser', password="testpass")
        response = self.client.post("/accounts/logout")
        self.assertEqual(response.status_code, 301)

    def test_logout_not_logged_in(self):
        response = self.client.post("/accounts/logout")
        self.assertEqual(response.status_code, 302)


class ProfileModelTests(BaseTestCase):
    '''
    Tests Profile model __str__
    '''

    def test_profile_model_str(self):
        user = User.objects.get(username='testuser')
        self.assertEqual(str(user.profile), user.username)
