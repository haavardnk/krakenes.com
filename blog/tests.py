from django.test import TestCase
from django.urls import reverse
from posts.models import BlogPost, Category, Tag
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.
class BaseTestCase(TestCase):
    '''
    Basic test setup for pages
    ''' 
    def setUp(self):
        user = User.objects.create_user(username='testuser', email='test@test.com', password='testpass')
        category = Category.objects.create(name='Test_cat')
        image = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
        for i in range(1,6):
            BlogPost.objects.create(id= i, author=user, title='test'+str(i), content='test', category=category, image=image, summary=str(i)+str(i)+str(i))

class HomePageTests(BaseTestCase):
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
    
    def test_home_page_contains_three_blogposts(self):
        '''
        Checks that the home page only contains the latest three blog posts
        '''
        response = self.client.get('/')
        for i in range(5, 2, -1):
            self.assertContains(response, BlogPost.objects.get(id=i).summary)
        self.assertNotContains(response, BlogPost.objects.get(id=2).summary)

class BlogPageTests(BaseTestCase):
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

    def test_blog_page_contains_four_blogposts(self):
        '''
        Checks that blog page contains correct amount of blog posts
        '''
        response = self.client.get('/blog/')
        for i in range(5, 1, -1):
            self.assertContains(response, BlogPost.objects.get(id=i).summary)
        self.assertNotContains(response, BlogPost.objects.get(id=1).summary)
    
    def test_blog_page_pagination(self):
        '''
        Checks that blog page contains correct amount of pages.
        '''
        response = self.client.get('/blog/')
        self.assertContains(response, '?page=1')
        self.assertContains(response, '?page=2')
        self.assertNotContains(response, '?page=3')

    def test_blog_page_search(self):
        '''
        Checks that a search for only returns correct post.
        Also checks for correct message to user.
        '''
        response = self.client.post('/blog/', {'search': 'test5'})
        self.assertContains(response, BlogPost.objects.get(id=5).summary)
        self.assertNotContains(response, BlogPost.objects.get(id=4).summary)
        self.assertNotContains(response, BlogPost.objects.get(id=3).summary)
        self.assertContains(response, "Search results for")

    def test_blog_page_search_no_results(self):
        '''
        Checks that a search with no results gives the right message.
        '''
        response = self.client.post('/blog/', {'search': 'thiswillgivenoresults'})
        self.assertContains(response, 'There are no results that match your search.')

    def test_blog_page_categories(self):
        '''
        Checks that the category shows and returns correct post count.
        '''
        response = self.client.get('/blog/')

        self.assertContains(response, '<a href="#">Test_cat</a><span>5</span>')