from django.contrib.auth.models import User
from django.urls import reverse
from django.test import LiveServerTestCase
from selenium import webdriver
import os
import time
from catalogue.models import Category, Product, Favorite_product
from catalogue.management.commands.enums import URL_OFF


username = 'Rititi'
email = 'ri.titi@mail.fr'
password = 'pNd9sdfi'
new_email = 'ri.tata@mail.fr'


class Test_favorite_product(LiveServerTestCase):
    def setUp(self):
        # Create db product
        category_01 = Category.objects.create(
            name="Plat léger"
        )
        img_link = URL_OFF + "images/products/317/658/201/6252/front_fr.59.400.jpg"
        product_01 = Product.objects.create(
            code="32",
            product_name="Fromage à raclette",
            nova_groups=4,
            nutrition_grades="D",
            stores="",
            picture_url=img_link,
            eco_score="C",
            energy_value=10.0,
            fat_value=12.2,
            sugar_value=324.1,
            fiber_value=73.1,
            protein_value=22.2,
            salt_value=924.2)

        product_01.categories.set([category_01])

        cod = 355
        img_link = URL_OFF + "images/products/359/669/013/6046/front_fr.39.400.jpg",
        for i in range(10):
            new_product = Product.objects.create(
                code=str(cod+i),
                product_name="Cordon bleu père Dodu",
                nova_groups=4,
                nutrition_grades="B",
                stores="",
                picture_url=img_link,
                eco_score="D",
                energy_value=32.0,
                fat_value=42.2,
                sugar_value=12.1,
                fiber_value=72.1,
                protein_value=14.2,
                salt_value=9.2)
            new_product.categories.set([category_01])

        # Create new user
        self.data = {
            'username': username,
            'email': email,
            'password': password,
        }
        self.user = User.objects.create_user(**self.data)

        root_dir = os.path.dirname(os.path.abspath(__file__))
        self.driver = webdriver.Firefox(
            executable_path=os.path.join(root_dir, 'geckodriver'))
        self.action = webdriver.ActionChains(self.driver)

        # Open the navigator with the server adress
        self.driver.get(self.live_server_url)

    def tearDown(self):
        self.driver.quit()

    def test_login(self):
        login = self.driver.find_element_by_id('login_button')
        login.click()
        self.driver.implicitly_wait(3)
        time.sleep(3)
        username_field = self.driver.find_element_by_id('id_username')
        username_field.send_keys(username)
        time.sleep(1)
        password_field = self.driver.find_element_by_id('id_password1')
        password_field.send_keys(password)
        time.sleep(2)
        button_ok = self.driver.find_element_by_id('login_validate')
        self.action.move_to_element(button_ok)
        time.sleep(2)
        button_ok.click()

        self.assertEqual(
            self.driver.current_url,
            self.live_server_url + reverse('home'))

        self.find_substitute()

    def find_substitute(self):
        search = self.driver.find_element_by_id('product_input')
        search_button = self.driver.find_element_by_id('search_button')
        query = 'Cordon'
        search.send_keys(query)
        self.action.move_to_element(search_button)
        self.driver.implicitly_wait(2)
        search_button.click()
        time.sleep(3)
        self.assertEqual(
            self.driver.current_url,
            self.live_server_url + reverse('result') + '?user_search=' + query)

        img_button = self.driver.find_elements_by_class_name('text-content')
        img_button[0].click()
        time.sleep(2)
        self.assertEqual(
            self.driver.current_url,
            self.live_server_url + reverse('result') + '?user_search=355')

        self.save_subsitute()

    def save_subsitute(self):
        queryset = Favorite_product.objects.filter(product='355')
        self.assertEqual(len(queryset), 0)

        save_button = self.driver.find_elements_by_id('save_button')[0]
        self.action.move_to_element(save_button)
        time.sleep(2)
        save_button.click()
        time.sleep(2)

        queryset = Favorite_product.objects.filter(product='355')
        self.assertEqual(len(queryset), 1)

        self.check_new_favorite()

    def check_new_favorite(self):
        favorite_button = self.driver.find_element_by_id('favorite_button')
        favorite_button.click()
        time.sleep(1)
        self.assertEqual(
            self.driver.current_url,
            self.live_server_url + reverse('favorite'))

        self.del_subsitute()

    def del_subsitute(self):
        del_button = self.driver.find_elements_by_id('delete_button')
        self.assertEqual(len(del_button), 1)

        del_button = del_button[0]
        self.action.move_to_element(del_button)
        time.sleep(2)
        del_button.click()
        time.sleep(2)

        queryset = Favorite_product.objects.filter(product='355')
        self.assertEqual(len(queryset), 0)

        self.user_logout()

    def user_logout(self):
        logout_button = self.driver.find_element_by_id('logout_button')
        logout_button.click()
        time.sleep(1)

        self.assertEqual(
            self.driver.current_url,
            self.live_server_url + reverse('home'))


class Test_change_email(LiveServerTestCase):
    def setUp(self):
        # Create new user
        self.data = {
            'username': username,
            'email': email,
            'password': password,
        }
        self.user = User.objects.create_user(**self.data)
        self.client.login(**self.data)

        root_dir = os.path.dirname(os.path.abspath(__file__))
        self.driver = webdriver.Firefox(
            executable_path=os.path.join(root_dir, 'geckodriver'))
        self.action = webdriver.ActionChains(self.driver)

        # Open the navigator with the server adress
        self.driver.get(self.live_server_url)

    def tearDown(self):
        self.driver.quit()

    def test_login(self):
        login = self.driver.find_element_by_id('login_button')
        login.click()
        self.driver.implicitly_wait(3)
        username_field = self.driver.find_element_by_id('id_username')
        username_field.send_keys(username)
        password_field = self.driver.find_element_by_id('id_password1')
        password_field.send_keys(password)
        button_ok = self.driver.find_element_by_id('login_validate')
        self.action.move_to_element(button_ok)
        button_ok.click()
        self.change_email()

    def change_email(self):
        login = self.driver.find_element_by_id('account_button')
        login.click()
        self.driver.implicitly_wait(3)
        time.sleep(3)
        change_button = self.driver.find_element_by_id('change_account_data')
        change_button.click()

        time.sleep(1)
        email_field = self.driver.find_element_by_id('email_input_1')
        email_field.send_keys(new_email)
        email_field = self.driver.find_element_by_id('email_input_confirm')
        time.sleep(1)
        email_field.send_keys(new_email)
        button_ok = self.driver.find_element_by_id('change_email_button')
        button_ok.click()
        time.sleep(2)

        self.assertEqual(
            User.objects.get(username=username).email,
            new_email)

        #email_field = self.driver.find_element_by_class_name('print-data')
        #self.assertEqual(email_field.innerText, new_email)
        self.delete_account()

    def delete_account(self):
        change_button = self.driver.find_element_by_id('change_account_data')
        change_button.click()
        button_delete_1 = self.driver.find_element_by_id('delete_account')
        button_delete_1.click()
        time.sleep(1)
        button_delete_2 = self.driver.find_element_by_id('delete_account_confirm')
        button_delete_2.click()
        time.sleep(1)

        self.assertEqual(
            User.objects.filter(username=username).count(),
            0)
