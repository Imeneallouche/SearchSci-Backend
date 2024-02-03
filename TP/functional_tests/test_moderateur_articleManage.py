from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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

            # Find the search link and click it
            search_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href^="/FilterArticles/"]'))
            )
            search_link.click()

            # Wait for the search results page to load (adjust wait time as needed)
            first_h1_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.text-xl.text-black.font-bold'))
            )
            time.sleep(10)


            # Retrieve text from the first h1 element with the specified class
           
            first_h1_text = first_h1_element.text

            # Verify the search results by checking the presence of the expected text
            expected_text = "Semantic Analysis and Classification of Emails through Informative Selection of Features and Ensemble AI Model"

            self.assertEqual(expected_text, first_h1_text)

        except Exception as e:
            self.fail(f"An error occurred: {e}")
