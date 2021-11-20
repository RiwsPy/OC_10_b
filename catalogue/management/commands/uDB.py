from django.core.management.base import BaseCommand
from .enums import HEADERS, PAYLOAD, CATEGORIES, URL_SEARCH
import requests
from catalogue.models import Product, Category
from django.db.models.deletion import ProtectedError


class Command(BaseCommand):
    help = 'Update database with OpenFoodFacts API'

    def handle(self, *args, **kwargs) -> None:
        self.call_api()
        self.stdout.write(
            self.style.SUCCESS('Mise à jour de la base de données réussie.'))

    def call_api(self) -> None:
        """
            Request OpenFoodFacts API
            Save the results in the database
        """

        code_set = set()
        print("Mise à jour de la base de données...")
        params = PAYLOAD.copy()
        for product in Product.objects.all():
            try:
                product.delete()
            except ProtectedError:
                pass

        for category in CATEGORIES:
            params["tag_0"] = category
            req = requests.get(URL_SEARCH, params=params, headers=HEADERS)
            if req.status_code != 200:
                continue

            results_json = req.json()
            cat = self.save_category(category)

            for product_data in results_json["products"]:
                if not product_data["code"] in code_set:
                    code_set.add(product_data["code"])
                    self.save_product(product_data, cat)

    def save_category(self, category_name: str) -> Category:
        return Category.objects.update_or_create(name=category_name[:200])[0]

    def save_product(self, product_data: dict, cat: Category) -> None:
        """
            Create the product, clean it and add it in database if possible
        """
        pro = Product()
        pro.clean(product_data)
        if pro.is_clean():
            pro = pro.update_or_create()
            pro.categories.add(cat)
            pro.save()
