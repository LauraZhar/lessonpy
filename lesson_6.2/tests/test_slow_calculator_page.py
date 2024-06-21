import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.slow_calculator_page import SlowCalculatorPage
import time

@pytest.fixture
def driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    yield driver
    driver.quit()

def test_calculator(driver):
    page = SlowCalculatorPage(driver)
    page.load()
    page.set_delay(45)
    page.perform_calculation()
    time.sleep(45)
    assert page.get_result_text() == "15"