from django.test import LiveServerTestCase
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class SeleniumTestCase(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Set up Chrome 
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')  # Run in headless mode
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # Init  driver
        cls.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()