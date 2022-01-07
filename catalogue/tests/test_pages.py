from django.test import TestCase
from django.urls.base import reverse
from catalogue.models import Product, Category, Favorite_product
from django.contrib.auth.models import User
from catalogue.management.commands.enums import URL_OFF

# Create your tests here.


class HomePage(TestCase):
    # ran before each test.
    def setUp(self):
        img_link = "images/products/317/658/201/6252/front_fr.59.400.jpg"
        category_01 = Category.objects.create(
            name="Plat léger"
        )
        product_01 = Product.objects.create(
            code="32",
            product_name="Fromage à raclette",
            nova_groups=4,
            nutrition_grades="D",
            stores="",
            picture_url=URL_OFF + img_link,
            eco_score="C",
            energy_value=10.0,
            fat_value=12.2,
            sugar_value=324.1,
            fiber_value=73.1,
            protein_value=22.2,
            salt_value=924.2)

        product_02 = Product.objects.create(
            code="355",
            product_name="Cordon bleu père Dodu",
            nova_groups=4,
            nutrition_grades="B",
            stores="",
            picture_url=URL_OFF + img_link,
            eco_score="D",
            energy_value=32.0,
            fat_value=42.2,
            sugar_value=12.1,
            fiber_value=72.1,
            protein_value=14.2,
            salt_value=9.2)

        product_01.categories.set([category_01])
        product_02.categories.set([category_01])

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_result_page_returns_ok(self):
        response = self.client.get(
            'http://127.0.0.1:8000/catalogue/?user_search=32')
        self.assertContains(
            response,
            'Vous pouvez remplacer cet aliment par :',
            status_code=200,
            html=False)

    def test_result_page_returns_no_result(self):
        response = self.client.get(
            'http://127.0.0.1:8000/catalogue/?user_search=33')
        self.assertContains(
            response,
            'Aucun produit ne correspond aux critères de recherche... :(',
            status_code=200,
            html=False)

    def test_display_details(self):
        response = self.client.get(
            'http://127.0.0.1:8000/catalogue/32/')

        self.assertTemplateUsed(response, 'catalogue/details.html')
        pro = Product.objects.get(pk='32')
        self.assertContains(
            response,
            pro.product_name,
            status_code=200,
            html=False)

        self.assertContains(
            response,
            'Repères nutritionnels pour 100g :',
            status_code=200,
            html=False)

        self.assertContains(
            response,
            'Nutri-score :',
            status_code=200,
            html=False)

    def test_paginate(self):
        category_x = Category.objects.create(
            name="Plat légers"
        )
        img_link = "images/products/359/669/013/6046/front_fr.39.400.jpg"
        product_x = {
            'code': "355",
            'product_name': "Cordon bleu père Dodu",
            'nova_groups': 4,
            'nutrition_grades': "B",
            'stores': "",
            'picture_url': URL_OFF + img_link,
            'eco_score': "D",
            'energy_value': 32.0,
            'fat_value': 42.2,
            'sugar_value': 12.1,
            'fiber_value': 72.1,
            'protein_value': 14.2,
            'salt_value': 9.2}

        for _ in range(10):
            product_x['code'] = str(int(product_x['code'])+1)
            pro = Product.objects.create(**product_x)
            pro.categories.set([category_x])

        response = self.client.get(
            'http://127.0.0.1:8000/catalogue/?user_search=r')
        self.assertContains(
            response,
            'Plusieurs résultats correspondent à vos critères de recherche :',
            status_code=200,
            html=False)

        for request_context in response.context:
            for dict_context in request_context:
                if 'paginate' in dict_context:
                    self.assertTrue(dict_context['paginate'])
                    self.assertEqual(len(dict_context['db']), 6)

        response = self.client.get(
            'http://127.0.0.1:8000/catalogue/?user_search=r&page=2')
        self.assertEqual(response.status_code, 200)


class Catalogue_without_login(TestCase):
    def test_save_product(self):
        response = self.client.get(reverse('save'))
        self.assertEqual(response.status_code, 302)

    def test_favorite_result_result(self):
        response = self.client.get(reverse('favorite'))
        self.assertEqual(response.status_code, 302)


username = 'testuser'
email = 'loulou@test.com'
password = 'Pxâ76jjs1Ps'


class Favorite_products(TestCase):
    def setUp(self):
        self.data = {
            'username': username,
            'email': email,
            'password': password,
        }
        self.user = User.objects.create_user(**self.data)
        self.client.login(**self.data)
        HomePage.setUp(self)

    def test_get_method(self):
        self.client.get(reverse('home'))
        self.client.get(reverse('save'))
        self.assertTemplateUsed('home.html')

    def test_save_product_ok(self):
        self.client.post(reverse('save'),
            {
            'product_search_id': "32",
            'substitute_id': "355"})
        self.assertEqual(Favorite_product.objects.filter(user_id=self.user).count(), 1)
        self.assertTemplateUsed('home.html')

    def test_save_product_fail_id_doesnt_exist(self):
        self.client.post(reverse('save'),
            {
            'product_search_id': "31",
            'substitute_id': "355"})
        self.assertEqual(Favorite_product.objects.filter(user_id=self.user).count(), 0)
        self.assertTemplateUsed('home.html')

    def test_save_product_fail_insuffisant_data(self):
        self.client.post(reverse('save'),
            {
            'product_search_id': "32"})
        self.assertEqual(Favorite_product.objects.filter(user_id=self.user).count(), 0)
        self.assertTemplateUsed('home.html')

    def test_delete_ok(self):
        self.client.post(reverse('save'),
            {
                'product_search_id': "32",
                'substitute_id': "355"
            })
        self.client.post(reverse('delete'),
            {
                'product_search_id': '',
                'substitute_id': '32'
            })
        self.assertEqual(Favorite_product.objects.filter(user_id=self.user).count(), 0)

    def test_delete_fail_wrong_data(self):
        self.client.post(reverse('save'),
            {
                'product_search_id': "32",
                'substitute_id': "355"
            })
        self.client.post(reverse('delete'),
            {
                'product_search_id': '354',
                'substitute_id': '31'
            })
        self.assertEqual(Favorite_product.objects.filter(user_id=self.user).count(), 1)

    def test_delete_fail_insuffisant_data(self):
        self.client.post(reverse('save'),
            {
                'product_search_id': "32",
                'substitute_id': "355"
            })
        self.client.post(reverse('delete'),
            {
            })
        self.assertEqual(Favorite_product.objects.filter(user_id=self.user).count(), 1)
