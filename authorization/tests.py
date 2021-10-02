from django.test import TestCase

from authorization.models import User

data1 = {
    'username': 'shammy296',
    'email': 'tets@tets.com',
    'phone': '+918091665739',
    'password': 'shammy123',
    'first_name': 'Shammy',
    'last_name': 'Singh'
}

data2 = {
    'username': 'shammy2961',
    'email': 'tets@tets.com',
    'phone': '+918091665739',
    'password': 'shammy123',
    'first_name': 'Shammy',
    'last_name': 'Singh'
}


class UserTestCase(TestCase):
    model_object = User.objects

    def test_add_user(self):
        instance = self.model_object.create_user(data1.get('username'), data1.get('email'), data1.get('password'))
        instance.first_name = data1.get('first_name')
        instance.last_name = data1.get('last_name')
        instance.contact = data1.get('phone')
        instance.save()

    def test_get_current_user(self):
        self.test_add_user()

        self.model_object.get(username=data1.get('username'))

    def test_update_user(self):
        self.test_add_user()

        instance = self.model_object.get(username=data1.get('username'))
        instance.first_name = data2.get('username')
        instance.last_name = data2.get('last_name')
        instance.contact = data2.get('phone')
        instance.save()

    def test_delete_user(self):
        self.test_add_user()

        self.model_object.get(username=data1.get('username')).delete()
