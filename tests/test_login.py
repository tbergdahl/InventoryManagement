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
        # 1. Create test user
        User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )

        # 2. Navigate to login page
        login_url = f"{self.live_server_url}/user_management/"
        self.driver.get(login_url)
        
        # 3. Debug: Print current URL
        print(f"Current URL: {self.driver.current_url}")

        try:
            # 4. Find elements using your exact HTML structure
            username = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            
            password = self.driver.find_element(By.NAME, "password")
            submit = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            
            # 5. Fill and submit form
            username.send_keys("testuser")
            password.send_keys("testpass123")
            submit.click()
            
            # 6. Verify login success
            time.sleep(2)  # Wait for redirect
            print(f"Post-login URL: {self.driver.current_url}")
            
            # Either check for URL change or page content
            self.assertNotIn("login", self.driver.current_url.lower())
            self.assertIn("Inventory List", self.driver.page_source)  # Adjust to your success text
            
        except Exception as e:
            self.driver.save_screenshot("login_failed.png")
            print("Login failed. Screenshot saved as login_failed.png")
            print("Page source:", self.driver.page_source[:1000])
            raise e