from django.test import Client, TestCase
from django.template.engine import Engine
from .models import MyUser


class LoginTest(TestCase):
    def setUp(self):
        user = MyUser.objects.create_user(
            email='foo@bar.com',
            first_name='Foo',
            last_name='Barsson',
            password='123', )
        self.client = Client()

    def is_login_page(self, response):
        """Assert that `response` is a successful Login page response."""
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'strecklista/login.html')

    def test_login_renders_form_unless_post(self):
        response = self.client.get('/login/')
        self.is_login_page(response)
        self.assertEquals(response.context['error_message'], None)

    def test_login_without_trailing_slash_works_too(self):
        response = self.client.get('/login')
        self.is_login_page(response)
        self.assertEquals(response.context['error_message'], None)

    def test_invalid_login_shows_error(self):
        response = self.client.post('/login/', {
            'username': 'foo@bar.com',
            'password': 'completely wrong',
        })
        self.is_login_page(response)
        for fragment in ['and/or', 'incorrect', 'password', 'username']:
            self.assertIn(fragment, response.context['error_message'])

    def test_invalid_login_preserves_url(self):
        url = '/login/?next=/foo%20bar'
        response = self.client.post(url, {
            'username': 'foo@bar.com',
            'password': 'completely wrong',
        })
        self.is_login_page(response)
        self.assertEquals(response.context['action'], url)

    def test_successful_login_redirects_to_index(self):
        response = self.client.post('/login/', {
            'username': 'foo@bar.com',
            'password': '123',
        })
        self.assertRedirects(response, '/')

    def test_redirects_to_next_if_specified(self):
        response = self.client.post('/login/?next=/other/path', {
            'username': 'foo@bar.com',
            'password': '123',
        })
        # Cannot use `assertRedirects` since that actually checks whether the
        # redirect target is successfully served.
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/other/path')
