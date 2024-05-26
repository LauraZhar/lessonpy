import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_calculator():
    browser = webdriver.Chrome()
    try:
        browser.get("https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")
        
        # Ввод значения 45 в поле delay
        delay_input = browser.find_element(By.ID, "delay")
        delay_input.clear()
        delay_input.send_keys("45")
        
        # Нажатие кнопок 7 + 8 =
        browser.find_element(By.XPATH, "//span[text()='7']").click()
        browser.find_element(By.XPATH, "//span[text()='+']").click()
        browser.find_element(By.XPATH, "//span[text()='8']").click()
        browser.find_element(By.XPATH, "//span[text()='=']").click()
        
        # Ожидание результата
        result = WebDriverWait(browser, 50).until(
            EC.text_to_be_present_in_element((By.XPATH, "//div[@class='screen']"), "15")
        )
        
        assert result, "Result is not 15"
    finally:
        browser.quit()

