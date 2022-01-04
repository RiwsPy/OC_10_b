from django.test import TestCase
from django.contrib.auth.models import User
from django.urls.base import reverse
from user.views import user_change_email

username = 'testuser'
email = 'loulou@test.com'
password = 'Pxâ76jjs1Ps'
new_email_good = 'lou-lou@test.com'
new_email_wrong = 'loulou@testcom'

class User_test(TestCase):
    def setUp(self):
        self.data = {
            'username': username,
            'email': email,
            'password': password,
        }
        self.user = User.objects.create_user(**self.data)
        self.user.save()
        self.client.login(**self.data)

    def user_login(self):
        pass
        #is_authenticated = self.client.login(username=username, password=password)
        #self.assertTrue(is_authenticated)

        #kwargs = self.data.copy()
        #kwargs['password1'] = kwargs['password']
        #self.client.post(reverse('login'), kwargs, follow=True)


    def test_create_user(self):
        self.assertEqual(self.user.username, username)
        self.assertEqual(self.user.email, email)
        self.assertTrue(self.user.is_authenticated)

    def test_account_page_status_code(self):
        response = self.client.get(reverse('account'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/account.html')

    def test_user_show_favorite_html(self):
        response = self.client.get(reverse('favorite'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalogue/result.html')

    def test_user_connected_cannot_register(self):
        response = self.client.get(reverse('register'))

        self.assertRedirects(response, '/')

    def test_change_email_ok(self):
        response = self.client.post(
            reverse('change_email'),
            {'user_new_email':new_email_good,
            'user_new_email_confirm':new_email_good})

        self.assertEqual(response.context['user'].email, new_email_good)

    def test_change_email_fail(self):
        # Emails empty
        user_change_email(self.user, '', '')
        self.assertEqual(self.user.email, email)

        # Emails don't match
        user_change_email(self.user, email, new_email_good)
        self.assertEqual(self.user.email, email)

        # Emails don't correct
        user_change_email(self.user, new_email_wrong, new_email_wrong)
        self.assertEqual(self.user.email, email)

    def test_delete_user_ok(self):
        response = self.client.post(reverse('delete_account'))
        self.assertEqual(User.objects.filter(username=username).count(), 0)

    def test_delete_user_fail(self):
        self.client.get(reverse('delete_account'))
        self.assertEqual(User.objects.filter(username=username).count(), 1)


class User_without_auto_login(TestCase):
    def test_login_page_status_code(self):
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/login.html')

    def test_account(self):
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 302)

    def test_favorite(self):
        response = self.client.get(reverse('favorite'))
        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_register_user(self):
        data = {
            'username': 'Colette',
            'email': 'lovepetitpois@rat.com',
            'password1': password,
            'password2': password,
        }
        response = self.client.post(reverse('register'), data, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, '/')

    def test_register_user_fail(self):
        data = {
            'username': 'Colette',
            'email': 'lovepetitpois@rat.com',
            'password1': password,
            'password2': password+'nope',
        }
        response = self.client.post(reverse('register'), data, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertTemplateUsed(response, 'user/register.html')
