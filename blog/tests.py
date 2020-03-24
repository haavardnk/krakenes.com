from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.sessions.middleware import SessionMiddleware
from posts.models import BlogPost, Category, Tag, Comment


from .views import post


class BaseTestCase(TestCase):
    '''
    Basic test setup for pages
    '''

    def setUp(self):
        user = User.objects.create_user(
            username='testuser', email='test@test.com', password='testpass')
        tag = Tag.objects.create(id=13, name='Test_tag')
        image = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
        category = Category.objects.create(id=11, name='Test_cat', image=image)
        for i in range(1, 8):
            blogpost = BlogPost.objects.create(id=i, author=user, title='test '+str(
                i), content='t', category=category, image=image, summary=str(i)+str(i)+str(i))
            blogpost.tags.add(tag)


class HomePageTests(BaseTestCase):
    '''
    Tests of the home page
    '''

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')

    def test_home_page_contains_six_blogposts(self):
        '''
        Checks that home page contains correct amount of blog posts
        '''
        response = self.client.get('/')
        for i in range(7, 1, -1):
            self.assertContains(response, BlogPost.objects.get(id=i).summary)
        self.assertNotContains(response, BlogPost.objects.get(id=1).summary)

    def test_home_page_pagination(self):
        '''
        Checks that home page contains correct amount of pages.
        '''
        response = self.client.get('/')
        self.assertContains(response, '?page=1')
        self.assertContains(response, '?page=2')
        self.assertNotContains(response, '?page=3')


class SearchPageTests(BaseTestCase):
    '''
    Tests of the search page
    '''

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/search.html')

    def test_search_page_search(self):
        '''
        Checks that a search for only returns correct post.
        Also checks for correct message to user.
        '''
        response = self.client.get('/search/', {'search': 'test 5'})
        self.assertContains(response, BlogPost.objects.get(id=5).title)
        self.assertNotContains(response, BlogPost.objects.get(id=4).title)
        self.assertNotContains(response, BlogPost.objects.get(id=3).title)

    def test_search_page_contains_six_blogposts(self):
        '''
        Checks that search page contains correct amount of blog posts
        '''
        response = self.client.get('/search/', {'search': 'test'})
        for i in range(7, 1, -1):
            self.assertContains(response, BlogPost.objects.get(id=i).summary)
        self.assertNotContains(response, BlogPost.objects.get(id=1).summary)

    def test_search_page_search_no_results(self):
        '''
        Checks that a search with no results gives the right message.
        '''
        response = self.client.get(
            '/search/', {'search': 'thiswillgivenoresults'})
        self.assertContains(
            response, 'There are no matching posts')

class PostPageTests(BaseTestCase):
    '''
    Tests of the post page
    '''

    def test_view_uses_correct_template(self):
        response = self.client.get('/blog/test-1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post.html')

    def test_post(self):
        '''
        Tests rendering of a post
        '''
        response = self.client.get('/blog/test-1/')
        self.assertContains(response, BlogPost.objects.get(id=1).title)
        self.assertContains(response, BlogPost.objects.get(id=1).content)
        self.assertContains(response, BlogPost.objects.get(id=1).image)
        self.assertContains(response, BlogPost.objects.get(
            id=1).pub_date.strftime('%e %b %Y'))
        self.assertContains(
            response, BlogPost.objects.get(id=1).author.username)
        self.assertContains(response, "Test_tag")

    def test_wrong_post_404(self):
        '''
        Tests requesting a post that does not exist
        '''
        response = self.client.get('/blog/1337/')
        self.assertEqual(response.status_code, 404)

    # def test_comment(self):
    #     '''
    #     Test posting a comment on a blog post while authenticated.
    #     '''
    #     self.request_factory = RequestFactory()
    #     self.user = User.objects.get(username='testuser')

    #     request = self.request_factory.post(
    #         '/blog/1/', {'comment': 'testcomment'})
    #     request.user = self.user

    #     middleware = SessionMiddleware()
    #     middleware.process_request(request)

    #     request.session.save()
    #     response = post(request, 1)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "testcomment")
    #     self.assertContains(response, "Comment submitted.")
    #     self.assertContains(response, "(1)")
    

class CategoryPageTests(BaseTestCase):
    '''
    Tests of the category page
    '''

    def test_view_uses_correct_template(self):
        response = self.client.get('/blog/category/Test_cat/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/category.html')

    def test_category_page_contains_six_blogposts(self):
        '''
        Checks that home page contains correct amount of blog posts
        '''
        response = self.client.get('/blog/category/Test_cat/')
        for i in range(7, 1, -1):
            self.assertContains(response, BlogPost.objects.get(id=i).summary)
        self.assertNotContains(response, BlogPost.objects.get(id=1).summary)

    def test_category_page_pagination(self):
        '''
        Checks that home page contains correct amount of pages.
        '''
        response = self.client.get('/blog/category/Test_cat/')
        self.assertContains(response, '?page=1')
        self.assertContains(response, '?page=2')
        self.assertNotContains(response, '?page=3')

class BlogPostModelTests(BaseTestCase):
    '''
    Tests BlogPost model __str__
    '''

    def test_blogpost_model_str(self):
        post = BlogPost.objects.get(id=1)
        self.assertEqual(str(post), "test 1")


class CategoryModelTests(BaseTestCase):
    '''
    Tests Category model __str__
    '''

    def test_category_model_str(self):
        category = Category.objects.get(id=11)
        self.assertEqual(str(category), "Test_cat")


class TagModelTests(BaseTestCase):
    '''
    Tests Tag model __str__
    '''

    def test_tag_model_str(self):
        Tag.objects.create(id=12, name='Test_tag')
        tag = Tag.objects.get(id=12)
        self.assertEqual(str(tag), "Test_tag")


class CommentModelTests(BaseTestCase):
    '''
    Tests Comment model __str__
    '''

    def test_comment_model_str(self):
        post = BlogPost.objects.get(id=1)
        user = User.objects.get(username='testuser')
        comment = Comment.objects.create(
            post=post, author=user, text="test_comment")
        self.assertEqual(str(comment), "test_comment")
