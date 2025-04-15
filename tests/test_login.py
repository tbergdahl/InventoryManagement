from django.test import LiveServerTestCase
from django.contrib.auth import get_user_model
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

User = get_user_model()

class LoginTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")  # Remove to see browser window
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_login(self):
        User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )

        login_url = f"{self.live_server_url}/user_management/"
        self.driver.get(login_url)
        
        print(f"Current URL: {self.driver.current_url}")

        try:
            username = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            
            password = self.driver.find_element(By.NAME, "password")
            submit = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            
            username.send_keys("testuser")
            password.send_keys("testpass123")
            submit.click()
            
            time.sleep(2)  
            print(f"Post-login URL: {self.driver.current_url}")
            
            self.assertNotIn("login", self.driver.current_url.lower())
            self.assertIn("Two-Factor Authentication", self.driver.page_source)  
            
        except Exception as e:
            self.driver.save_screenshot("login_failed.png")
            print("Login failed. Screenshot saved as login_failed.png")
            print("Page source:", self.driver.page_source[:1000])
            raise e
        
class InvalidLoginTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")  # Remove this line to see the browser
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_invalid_login(self):
        login_url = f"{self.live_server_url}/user_management/"
        self.driver.get(login_url)

        print(f"Current URL: {self.driver.current_url}")

        try:
            username = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            password = self.driver.find_element(By.NAME, "password")
            submit = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            username.send_keys("nonexistentuser")
            password.send_keys("wrongpassword")
            submit.click()

            time.sleep(2)  # Wait for page to load
            self.assertIn("Login", self.driver.page_source) # are we still on login page?
            self.assertIn("Invalid", self.driver.page_source)

        except Exception as e:
            self.driver.save_screenshot("invalid_login_failed.png")
            print("Test failed. Screenshot saved as invalid_login_failed.png")
            print("Page source:", self.driver.page_source[:1000])
            raise e