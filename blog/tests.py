from django.test import TestCase
from django.urls import reverse
from posts.models import BlogPost, Category
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.
class BaseTestClass(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', email='test@test.com', password='testpass')
        category = Category.objects.create(name='Automation')
        image = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
        for i in range(1,6):
            BlogPost.objects.create(author=user, title='test'+str(i), content='test', category=category, image=image)

class HomePageTests(BaseTestClass):
    '''
    Tests of the home page
    ''' 

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
    
    def test_home_page_contains_three_blogposts(self):
        response = self.client.get('/')
        posts = BlogPost.objects.all()
        for i in range(0,3):
            self.assertContains(response, posts[i].title)
        self.assertNotContains(response, posts[3].title)

class BlogPageTests(BaseTestClass):
    '''
    Tests of the blog page
    '''
    def test_blog_page_status_code(self):
        response = self.client.get('/blog/')
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('blog'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog.html')

    def test_blog_page_contains_correct_html(self):
        response = self.client.get('/blog/')
        self.assertContains(response, 'Search the blog')

    def test_blog_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/blog/')
        self.assertNotContains(
            response, 'Not in blog')

    def test_blog_page_contains_four_blogposts(self):
        response = self.client.get('/blog/')
        posts = BlogPost.objects.all()
        for i in range(0,4):
            self.assertContains(response, posts[i].title)
        self.assertNotContains(response, posts[4].title)
    
    def test_blog_page_contains_one_post_on_page_two(self):
        response = self.client.get('/blog/?page=2/')
        # posts = BlogPost.objects.all()
        # self.assertContains(response, posts[4].title)
        self.assertContains(response, '?page=1')
        self.assertContains(response, '?page=2')
        self.assertNotContains(response, '?page=3')