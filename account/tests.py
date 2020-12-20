from django.test import TestCase
from .models import User
from django.test import Client


class UserModelTest(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(email='mohsn@example.com', full_name='Mohsn Mohsni', password='mohsn')
        User.objects.create_user(email='mina@example.com', full_name='Mina Mohamadi', password='mina')
        User.objects.create_user(email='ali@example.com', full_name='Ali Alae', password='ali')
        User.objects.create_superuser(email='hospin@example.com', full_name='Hospin Roman', password='hospin')

    def test_user(self):
        mohsn = User.objects.get(email='mohsn@example.com')
        mina = User.objects.get(email='mina@example.com')
        ali = User.objects.get(email='ali@example.com')
        hospin = User.objects.get(email='hospin@example.com')
        self.assertEqual(mohsn.full_name, 'Mohsn Mohsni')
        self.assertNotEqual(mohsn.password, 'mohsn')
        self.assertEqual(mina.is_active, True)
        self.assertEqual(mina.is_staff, False)
        self.assertEqual(ali.get_full_name(), 'Ali Alae')
        self.assertEqual(ali.__str__(), 'Ali Alae')
        self.assertEqual(hospin.is_superuser, True)
        self.assertEqual(hospin.is_staff, True)


class UserViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_user(self):
        get_response1 = self.client.get('/auth/login/')
        self.assertEqual(get_response1.status_code, 200)
        post_response1 = self.client.post('/auth/login/', email='mohsn@gmail.com', password='mohsn')
        self.assertEqual(post_response1.status_code, 200)
        get_response2 = self.client.get('/auth/logout/')
        self.assertEqual(get_response2.status_code, 200)
        get_response3 = self.client.get('/auth/register/')
        self.assertEqual(get_response3.status_code, 200)
        post_response3 = self.client.post('/auth/register/', email='mohsn@gmail.com', password='mohsn')
        self.assertEqual(post_response3.status_code, 200)
