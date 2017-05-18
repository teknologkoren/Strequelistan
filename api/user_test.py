from django.test import Client, TestCase
from strecklista.models import MyUser
import json


class UserTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = MyUser.objects.create_user(
            email='foo@bar.com',
            first_name='Foo',
            last_name='Barsson',
            password='123', )
        self.other_user = MyUser.objects.create_user(
            email='ann@other.org',
            first_name='Ann',
            last_name='Other',
            password='abc', )
        self.client.force_login(self.user)

    def get_json(self, path):
        return json.loads(self.client.get(path).content.decode())

    def get_own_data(self):
        return self.get_json('/api/user/1/')

    def test_can_access_own_balance(self):
        self.assertIn('balance', self.get_own_data())

    def test_balance_is_an_integer(self):
        balance = self.get_own_data()['balance']
        self.assertEquals(type(balance), int)

    def test_cannot_access_another_persons_balance(self):
        data = self.get_json('/api/user/2/')
        self.assertNotIn('balance', data)
