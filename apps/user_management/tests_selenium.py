from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
from django.contrib.auth import get_user_model
from apps.inventory.models import InventoryItem, ThresholdSetting  
from django.utils.timezone import now, timedelta

class UserLoginAndInventoryTest(LiveServerTestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_superuser(
            username='adminuser',
            password='Sh0wP@ss*90',
            email='shampurna.das@wsu.edu',
            usertype='ADMIN'  
        )

        #  Create dummy threshold
        self.threshold = ThresholdSetting.objects.create(
            product='Milk',
            min_quantity=10,
            max_quantity=50,
            color='red',
            template_message="Stock low: {stock} left!"
        )

        #  Create dummy inventory
        InventoryItem.objects.create(
            name='Milk',
            category='dairy',
            count=5,  # deliberately low to trigger alert
            expiry_date=now().date() - timedelta(days=1),  # expired date
            min_quantity=10,
            max_quantity=50,
            template_message="Stock low: {stock} left!"
        )

    def test_full_user_flow(self):
        driver = webdriver.Safari()

        try:
            driver.get(self.live_server_url)
            time.sleep(2)

            #  First, check Forgot Password Link
            forgot_link = driver.find_element(By.LINK_TEXT, "Forgot your password?")
            forgot_link.click()
            time.sleep(2)
            self.assertIn("Forgot Your Password", driver.page_source)

            # Now go back to Login page manually
            driver.back()
            time.sleep(2)

            # Login
            username_input = driver.find_element(By.NAME, "username")
            password_input = driver.find_element(By.NAME, "password")
            username_input.send_keys('adminuser')
            password_input.send_keys('Sh0wP@ss*90')
            driver.find_element(By.TAG_NAME, "button").click()
            time.sleep(3)

            #  Handle 2FA if needed
            if "Enter OTP" in driver.page_source or "OTP" in driver.page_source:
                otp_input = driver.find_element(By.NAME, "otp")
                otp_input.send_keys(os.environ.get("TESTING_OTP", "12345"))
                driver.find_element(By.TAG_NAME, "button").click()
                time.sleep(3)

            #  Now check if dashboard loaded
            page_source = driver.page_source
            self.assertTrue(
                "Inventory Overview" in page_source or 
                "Pie Chart" in page_source or 
                "Sales Line Chart" in page_source
            )

            #  Click Inventory tab (optional)
            try:
                inventory_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Inventory")
                inventory_link.click()
                time.sleep(2)
            except:
                pass

            #  Click Thresholds tab (optional)
            try:
                thresholds_link = driver.find_element(By.LINK_TEXT, "Manage Thresholds")
                thresholds_link.click()
                time.sleep(2)
            except:
                pass

            #  Check for inventory alerts 
            page_source = driver.page_source
            self.assertTrue("⚠️" in page_source or "❗" in page_source)

        finally:
            driver.quit()
