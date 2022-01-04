from django.test import TestCase
from catalogue.management.commands.uDB import Command
from unittest.mock import patch
from catalogue.models import Category, Product
from json import load
from catalogue.management.commands.enums import HEADERS, PAYLOAD,\
    CATEGORIES, URL_SEARCH, URL_OFF
from django.db.utils import DataError
from pathlib import Path
import os


class Test_ImportAPIData(TestCase):
    def test_save_ok_product_and_category(self):
        category_01 = Category.objects.create(
            name="Plat léger"
        )
        img_link = "images/products/317/658/201/6252/front_fr.59.400.jpg"
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

        product_01.categories.set([category_01])

        self.assertEqual(len(Category.objects.all()), 1)
        self.assertEqual(len(Product.objects.all()), 1)

    def test_save_nope_product_and_category(self):
        img_link = "images/products/359/669/013/6046/front_fr.39.400.jpg"
        product_02 = {
            'code': "355",
            'product_name': "Cordon bleu père Dodu" + "o"*200,
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

        with self.assertRaisesMessage(
                DataError,
                ''):
            Product.objects.create(**product_02)

    @patch('requests.get')
    def test_request_ok_call_api(self, mock_request):
        mock_request.return_value.status_code = 200
        with open(
                os.path.join(
                    Path(__file__).resolve().parent,
                    "db_product_mock.json")) as file:
            file = load(file)
        mock_request.return_value.json.return_value = file

        Command().handle()
        params = PAYLOAD.copy()
        params['tag_0'] = "Boissons"

        mock_request.assert_called_with(
            URL_SEARCH,
            params=params,
            headers=HEADERS
        )

        self.assertEqual(len(Category.objects.all()), len(CATEGORIES))
        self.assertEqual(len(Product.objects.all()), 23)
