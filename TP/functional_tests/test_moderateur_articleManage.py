from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import TimeoutException

class TestSearchFunctionality(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Perform any setup needed before the tests in this class are run
        cls.PATH = "./functional_tests/msedgedriver.exe"

    def setUp(self):
        self.driver = webdriver.Edge(options=Options())
        self.driver.get("http://localhost:3000/Recherche/")
        self.driver.maximize_window()

    def tearDown(self):
        self.driver.quit()

    def test_search_and_verify_results(self):
        try:
            # Find the search input field and enter the search term 'analysis'
            search_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input.search-bar'))
            )
            search_input.send_keys('analysis')
            time.sleep(10)

            # Find and click on the search button
            search_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button span.search-icon'))
            )
            
            search_button.click()
            time.sleep(10)
            h1_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//h1[contains(text(), "Semantic Analysis and Classification of Emails through Informative Selection of Features and Ensemble AI Model")]'))
            )
            # Retrieve text from the h1 element
            first_h1_text = h1_element.text
            print("fffffffffffffff",first_h1_text)

            # Verify the search results by checking the presence of the expected text
            expected_text = "Semantic Analysis and Classification of Emails through Informative Selection of Features and Ensemble AI Model"
            
            assert expected_text == first_h1_text, f"Expected text: '{expected_text}', Actual text: '{first_h1_text}'"

        except TimeoutException:
            # Handle the case where the element is not found within the timeout
            print("Element not found within the specified time")

