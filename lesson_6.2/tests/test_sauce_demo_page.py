import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.swag_labs_page import SwagLabsPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    yield driver
    driver.quit()

def test_swag_purchase(driver):
    page = SwagLabsPage(driver)
    page.load()
    page.login("standard_user", "secret_sauce")
    page.add_products_to_cart()
    page.proceed_to_checkout()
    page.fill_checkout_form("Имя", "Фамилия", "123456")

    total_price = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(page.total_label)
    ).text

    assert total_price == "Total: $58.29", f"Unexpected total price: {total_price}"