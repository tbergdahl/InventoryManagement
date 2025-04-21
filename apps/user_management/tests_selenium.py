from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class UserLoginTest(LiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Safari()

    def tearDown(self):
        self.driver.quit()

    def test_login_2fa_and_forgot_password(self):
        driver = self.driver
        driver.get(self.live_server_url + "/login/")  # Your login page URL

        # Step 1: Login page
        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")
        username_input.send_keys("your_test_username")
        password_input.send_keys("your_test_password")
        password_input.send_keys(Keys.RETURN)

        # Wait for 2FA page to load
        time.sleep(2)

        # Step 2: 2FA page
        otp_input = driver.find_element(By.NAME, "otp")
        otp_input.send_keys("123456")  # ⚡ You should mock or pre-set a test OTP
        otp_input.send_keys(Keys.RETURN)

        time.sleep(2)

        # After successful 2FA, user should land on dashboard
        self.assertIn("Dashboard", driver.page_source)

        # Step 3: Check Forgot Password
        driver.get(self.live_server_url + "/password_reset/")

        email_input = driver.find_element(By.NAME, "email")
        email_input.send_keys("testuser@example.com")
        email_input.send_keys(Keys.RETURN)

        time.sleep(2)

        # After submitting, check for success message
        self.assertIn("password reset", driver.page_source.lower())
