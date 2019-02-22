from django.test import TestCase
from django.urls import reverse
from posts.models import BlogPost, Category
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.

class HomePageTests(TestCase):
    '''
    Tests of the home page
    '''
    def setUp(self):
        user = User.objects.create_user(username='testuser', email='test@test.com', password='testpass')
        category = Category.objects.create(name='Automation')
        image = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
        BlogPost.objects.create(author=user, title='test1', content='test', category=category, image=image)
        BlogPost.objects.create(author=user, title='test2', content='test', category=category, image=image)
        BlogPost.objects.create(author=user, title='test3', content='test', category=category, image=image)
        BlogPost.objects.create(author=user, title='test4', content='test', category=category, image=image)
        
    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')

    def test_home_page_contains_correct_html(self):
        response = self.client.get('/')
        self.assertContains(response, '<h1>Håvard Kråkenes  - Automation</h1>')

    def test_home_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/')
        self.assertNotContains(
            response, 'Not in home')
    
    def test_home_page_contains_blogposts(self):
        response = self.client.get('/')
        for i in range(1,4):
            self.assertContains(response, BlogPost.objects.get(id=i).title)
        self.assertNotContains(response, BlogPost.objects.get(id=4).title)