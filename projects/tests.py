from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from projects.models import Project
from posts.models import Category


class BaseTestCase(TestCase):
    '''
    Basic test setup for pages
    '''

    def setUp(self):
        user = User.objects.create_user(
            username='testuser', email='test@test.com', password='testpass')
        category = Category.objects.create(name='Test_cat')
        image = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
        for i in range(1, 6):
            Project.objects.create(id=i, author=user, title='test'+str(
                i), content='test', category=category, image=image, summary=str(i)+str(i)+str(i))


class ProjectsPageTests(BaseTestCase):
    '''
    Tests of the project page
    '''

    def test_view_uses_correct_template(self):
        response = self.client.get('/projects/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/projects.html')

    # def test_projects_page_contains_four_projects(self):
    #     '''
    #     Checks that project page contains correct amount of projects
    #     '''
    #     response = self.client.get('/projects/')
    #     for i in range(5, 1, -1):
    #         self.assertContains(response, Project.objects.get(id=i).title)
    #         self.assertContains(response, Project.objects.get(id=i).summary)
    #     self.assertNotContains(response, Project.objects.get(id=1).title)
    #     self.assertNotContains(response, Project.objects.get(id=1).summary)

    # def test_projects_page_pagination(self):
    #     '''
    #     Checks that projects page contains correct amount of pages.
    #     '''
    #     response = self.client.get('/projects/')
    #     self.assertContains(response, '?page=1')
    #     self.assertContains(response, '?page=2')
    #     self.assertNotContains(response, '?page=3')


class ProjectDetailPageTests(BaseTestCase):
    '''
    Tests of the project detail page
    '''

    def test_project_details(self):
        '''
        Tests rendering of a project
        '''
        response = self.client.get('/projects/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/project_details.html')
        self.assertContains(response, Project.objects.get(id=1).title)
        self.assertContains(response, Project.objects.get(id=1).content)
        self.assertContains(response, Project.objects.get(id=1).image)
        self.assertContains(response, Project.objects.get(
            id=1).pub_date.strftime('%e %b | %Y'))
        self.assertContains(
            response, Project.objects.get(id=1).author.username)
        self.assertContains(response, "Test_cat")

    def test_wrong_project_404(self):
        '''
        Tests requesting a project that does not exist
        '''
        response = self.client.get('/projects/1337/')
        self.assertEqual(response.status_code, 404)


class ProjectModelTests(BaseTestCase):
    '''
    Tests Project model __str__
    '''

    def test_project_model_str(self):
        project = Project.objects.get(id=1)
        self.assertEqual(str(project), "test1")
