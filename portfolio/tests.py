from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.sessions.middleware import SessionMiddleware
from .models import Album, Photo, Site

class BaseTestCase(TestCase):
    '''
    Basic test setup for pages
    '''

    def setUp(self):
        user = User.objects.create_user(
            username='testuser2', email='test2@test.com', password='testpass2')
        image1 = SimpleUploadedFile(name='foo1.gif', content=b'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00')
        image2 = SimpleUploadedFile(name='foo2.gif', content=b'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00')
        album = Album.objects.create(id=11, title='test album', image=image1)
        site = Site.objects.create(site_name='home', title='test')
        # photo1 = Photo.objects.create(id=1, title='test_photo1', photo_full=image1, front_page=True)
        # photo2 = Photo.objects.create(id=2, title='test_photo2', photo_full=image2, album=album, front_page=False)
        # photo3 = Photo.objects.create(id=3, title='test_photo3', photo_full=image2, front_page=True)


class HomePageTests(BaseTestCase):
    '''
    Tests of the home page
    '''

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/home.html')

