# from django.test import LiveServerTestCase
# from djoser.conf import User
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# import time

# from product.models import Category, Product
# from register.models import UserProfile


# class SeleniumTests(LiveServerTestCase):

#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.selenium = webdriver.Chrome()
#         cls.selenium.implicitly_wait(20)

#     @classmethod
#     def tearDownClass(cls):
#         cls.selenium.quit()
#         super().tearDownClass()

#     def setUp(self):
#         self.user = User.objects.create_user(username='test1', password='haslo12345')
#         # Jeśli chcesz, możesz również dodać dane do profilu użytkownika:
#         self.user_profile = UserProfile.objects.create(
#             user=self.user,
#             full_name='Test User',
#             email='test@example.com',
#             address='123 Test Street',
#             phone='1234567890',
#             city='Test City',
#             state='Test State',
#             zipcode='12345',
#             country='Test Country'
#         )

#         # Utworzenie kategorii testowej
#         self.category = Category.objects.create(name='Test Category', slug='test-category')

#         # Utworzenie produktów testowych
#         self.product1 = Product.objects.create(
#             category=self.category,
#             name='Test Product 1',
#             slug='test-product-1',
#             description='Description for test product 1',
#             price='9.99',
#             image='images/test-image.jpg',  # Tutaj podaj ścieżkę do obrazu, który chcesz przetestować
#             thumbnail='images/test-thumbnail.jpg',  # Tutaj podaj ścieżkę do miniatury obrazu, który chcesz przetestować
#             date_added='2022-01-01 12:00:00'
#         )
#         self.product2 = Product.objects.create(
#             category=self.category,
#             name='Test Product 2',
#             slug='test-product-2',
#             description='Description for test product 2',
#             price='19.99',
#             image='images/test-image2.jpg',  # Tutaj podaj ścieżkę do obrazu, który chcesz przetestować
#             thumbnail='images/test-thumbnail2.jpg',  # Tutaj podaj ścieżkę do miniatury obrazu, który chcesz przetestować
#             date_added='2022-01-01 12:00:00'
#         )
#         self.product3 = Product.objects.create(
#             category=self.category,
#             name='Test Product 3',
#             slug='test-product-3',
#             description='Description for test product 3',
#             price='29.99',
#             image='images/test-image3.jpg',  # Tutaj podaj ścieżkę do obrazu, który chcesz przetestować
#             thumbnail='images/test-thumbnail3.jpg',  # Tutaj podaj ścieżkę do miniatury obrazu, który chcesz przetestować
#             date_added='2022-01-01 12:00:00'
#         )

#     ####################### Login ########################
#     def test_home_page(self):
#         self.selenium.get('%s%s' % (self.live_server_url, '/'))
#         assert 'Sklep z ubraniami' in self.selenium.title

#     def test_login_title(self):
#         self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
#         assert 'Logowanie' in self.selenium.title

#     def test_login_isLoginText(self):
#         self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
#         assert 'Zaloguj się' in self.selenium.page_source

#     def test_login_isSubmitButton(self):
#         self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
#         try:
#             login_button = self.selenium.find_element(By.XPATH,
#                                                       "//button[@type='submit' and contains(text(), 'Zaloguj')]")
#             assert login_button is not None
#         except Exception as e:
#             self.fail(f"Login button not found: {e}")

#     def test_login_isUsernameInput(self):
#         try:
#             username_input = self.selenium.find_element(By.XPATH,
#                                                         "//input[@type='text' and @name='username' and @id='id_username']")
#             assert username_input is not None
#         except Exception as e:
#             self.fail(f"Username input not found: {e}")

#     def test_login_isPasswordInput(self):
#         try:
#             password_input = self.selenium.find_element(By.XPATH,
#                                                         "//input[@type='password' and @name='password' and @id='id_password']")
#             assert password_input is not None
#         except Exception as e:
#             self.fail(f"Password input not found: {e}")

#     def test_login_inputs(self):
#         self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
#         username_input = self.selenium.find_element(By.NAME, "username")
#         password_input = self.selenium.find_element(By.NAME, "password")
#         username_input.send_keys('test1')
#         password_input.send_keys('haslo12345')

#         assert username_input.get_attribute('value') == 'test1'
#         assert password_input.get_attribute('value') == 'haslo12345'

#         # password_input.send_keys(Keys.RETURN)
#         # time.sleep(2)  # Wait for the page to load
#         # print(self.selenium.page_source)
#         # assert 'Wyloguj się' in self.selenium.page_source
#         # assert username_input.get_attribute('value') == 'test1'
#         # assert password_input.get_attribute('value') == 'haslo12345'

#     def test_login(self):
#         self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
#         username_input = self.selenium.find_element(By.NAME, "username")
#         password_input = self.selenium.find_element(By.NAME, "password")
#         username_input.send_keys('test1')
#         password_input.send_keys('haslo12345')
#         # time.sleep(5)
#         login_button = self.selenium.find_element(By.XPATH, "//button[@type='submit' and contains(text(), 'Zaloguj')]")
#         login_button.click()
#         time.sleep(5)
#         assert 'Wyloguj się' in self.selenium.page_source

#     def test_logout(self):
#         self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
#         username_input = self.selenium.find_element(By.NAME, "username")
#         password_input = self.selenium.find_element(By.NAME, "password")
#         username_input.send_keys('test1')
#         password_input.send_keys('haslo12345')
#         # time.sleep(5)
#         login_button = self.selenium.find_element(By.XPATH, "//button[@type='submit' and contains(text(), 'Zaloguj')]")
#         login_button.click()
#         time.sleep(5)
#         assert 'Wyloguj się' in self.selenium.page_source

#         # Wylogowanie się po teście
#         logout_button = self.selenium.find_element(By.XPATH, "//input[@type='submit' and @value='Wyloguj się']")
#         logout_button.click()
#         time.sleep(5)  # Poczekaj na załadowanie nowej strony

#         # Sprawdzenie czy wylogowanie się powiodło
#         # assert 'Login' in self.selenium.page_source  # Przykład sprawdzania obecności przycisku "Login"

#         assert 'Zaloguj się' in self.selenium.page_source

#     ####################### Register ########################

#     def test_register_title(self):
#         self.selenium.get('%s%s' % (self.live_server_url, '/register/'))
#         assert 'Tworzenie konta' in self.selenium.title

#     def test_register_isLoginText(self):
#         self.selenium.get('%s%s' % (self.live_server_url, '/register/'))
#         assert 'Zaloguj się' in self.selenium.page_source
#         assert 'Zarejestruj' in self.selenium.page_source

#     def test_register_has_username_input(self):
#         self.selenium.get('%s%s' % (self.live_server_url, '/register/'))
#         try:
#             username_input = self.selenium.find_element(By.XPATH,
#                                                         "//input[@type='text' and @name='username' and @id='id_username']")
#             assert username_input is not None
#         except Exception as e:
#             self.fail(f"Username input not found: {e}")

#     def test_register_has_password1_input(self):
#         self.selenium.get('%s%s' % (self.live_server_url, '/register/'))
#         try:
#             password1_input = self.selenium.find_element(By.XPATH,
#                                                          "//input[@type='password' and @name='password1' and @id='id_password1']")
#             assert password1_input is not None
#         except Exception as e:
#             self.fail(f"Password1 input not found: {e}")

#     def test_register_has_password2_input(self):
#         self.selenium.get('%s%s' % (self.live_server_url, '/register/'))
#         try:
#             password2_input = self.selenium.find_element(By.XPATH,
#                                                          "//input[@type='password' and @name='password2' and @id='id_password2']")
#             assert password2_input is not None
#         except Exception as e:
#             self.fail(f"Password2 input not found: {e}")

#     def test_register_has_submitButton_input(self):
#         self.selenium.get('%s%s' % (self.live_server_url, '/register/'))
#         try:
#             password2_input = self.selenium.find_element(By.XPATH,
#                                                          "//button[@type='submit' and contains(text(), 'Zarejestruj')]")
#             assert password2_input is not None
#         except Exception as e:
#             self.fail(f"Submit button not found: {e}")

#     def test_register_inputs(self):
#         self.selenium.get('%s%s' % (self.live_server_url, '/register/'))
#         username_input = self.selenium.find_element(By.NAME, "username")
#         password1_input = self.selenium.find_element(By.NAME, "password1")
#         password2_input = self.selenium.find_element(By.NAME, "password2")
#         username_input.send_keys('KacperTest')
#         password1_input.send_keys('KacperTest123')
#         password2_input.send_keys('KacperTest123')

#         assert username_input.get_attribute('value') == 'KacperTest'
#         assert password1_input.get_attribute('value') == 'KacperTest123'
#         assert password2_input.get_attribute('value') == 'KacperTest123'

#     def test_register(self):
#         self.selenium.get('%s%s' % (self.live_server_url, '/register/'))
#         username_input = self.selenium.find_element(By.NAME, "username")
#         password1_input = self.selenium.find_element(By.NAME, "password1")
#         password2_input = self.selenium.find_element(By.NAME, "password2")
#         username_input.send_keys('KacperTest')
#         password1_input.send_keys('asdfghjkl!1')
#         password2_input.send_keys('asdfghjkl!1')
#         # time.sleep(5)
#         register_button = self.selenium.find_element(By.XPATH,
#                                                      "//button[@type='submit' and contains(text(), 'Zarejestruj')]")
#         register_button.click()
#         time.sleep(5)

#         self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
#         username_input = self.selenium.find_element(By.NAME, "username")
#         password_input = self.selenium.find_element(By.NAME, "password")
#         username_input.send_keys('KacperTest')
#         password_input.send_keys('asdfghjkl!1')
#         # time.sleep(5)
#         login_button = self.selenium.find_element(By.XPATH, "//button[@type='submit' and contains(text(), 'Zaloguj')]")
#         login_button.click()
#         time.sleep(5)
#         assert 'Wyloguj się' in self.selenium.page_source

#         # Wylogowanie się po teście
#         logout_button = self.selenium.find_element(By.XPATH, "//input[@type='submit' and @value='Wyloguj się']")
#         logout_button.click()
#         time.sleep(5)  # Poczekaj na załadowanie nowej strony

#         # Sprawdzenie czy wylogowanie się powiodło
#         # assert 'Login' in self.selenium.page_source  # Przykład sprawdzania obecności przycisku "Login"

#         assert 'Zaloguj się' in self.selenium.page_source
#         # assert 'Wyloguj się' in self.selenium.page_source

#     ####################### Products ########################
#     def test_products_show(self):
#         self.selenium.get('%s%s' % (self.live_server_url, '/'))
#         assert 'Test Product 1' in self.selenium.page_source
#         assert 'Test Product 2' in self.selenium.page_source
#         assert 'Test Product 3' in self.selenium.page_source
#         # time.sleep(20)

#     def test_product_show_detailed(self):
#         self.selenium.get('%s%s' % (self.live_server_url, '/'))
#         # Znalezienie i kliknięcie linku do produktu
#         try:
#             product_link = self.selenium.find_element(By.XPATH, "//a[@href='/product/1' and @class='card w-100 h-100']")
#             product_link.click()
#             time.sleep(2)  # Poczekaj na załadowanie nowej strony
#         except Exception as e:
#             self.fail(f"Product link not found or could not be clicked: {e}")

#         # Sprawdzenie czy strona produktu się załadowała
#         assert 'Test Product 1' in self.selenium.page_source
#         assert 'Description for test product 1' in self.selenium.page_source # Jest tylko na stronie konkretnego produktu