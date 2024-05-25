import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_swag_purchase():
    browser = webdriver.Chrome()
    try:
        browser.get("https://www.saucedemo.com/")

        # Авторизация
        browser.find_element(By.ID, "user-name").send_keys("standard_user")
        browser.find_element(By.ID, "password").send_keys("secret_sauce")
        browser.find_element(By.ID, "login-button").click()

        # Добавление товаров в корзину
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))
        ).click()
        browser.find_element(By.ID, "add-to-cart-sauce-labs-bolt-t-shirt").click()
        browser.find_element(By.ID, "add-to-cart-sauce-labs-onesie").click()

        # Переход в корзину
        browser.find_element(By.ID, "shopping_cart_container").click()

        # Оформление заказа
        browser.find_element(By.ID, "checkout").click()
        browser.find_element(By.ID, "first-name").send_keys("Имя")
        browser.find_element(By.ID, "last-name").send_keys("Фамилия")
        browser.find_element(By.ID, "postal-code").send_keys("123456")
        browser.find_element(By.ID, "continue").click()

        # Ожидание и получение итоговой суммы
        total_price = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "summary_total_label"))
        ).text

        # Проверка итоговой суммы
        assert total_price == "Total: $58.29", f"Unexpected total price: {total_price}"
    finally:
        browser.quit()
