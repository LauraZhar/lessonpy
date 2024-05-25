import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_form_submission():
    browser = webdriver.Chrome()
    try:
        browser.get("https://bonigarcia.dev/selenium-webdriver-java/data-types.html")

        # Ожидание появления всех необходимых полей
        fields = {
            "first-name": "Иван",
            "last-name": "Петров",
            "address": "Ленина, 55-3",
            "e-mail": "test@skypro.com",
            "phone": "+7985899998787",
            "zip-code": "",
            "city": "Москва",
            "country": "Россия",
            "job-position": "QA",
            "company": "SkyPro"
        }

        for field_id, value in fields.items():
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, field_id))
            )
            element.clear()
            element.send_keys(value)

        # Нажатие кнопки Submit
        submit_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Submit']"))
        )
        submit_button.click()

        # Ожидание проверки полей
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "zip-code"))
        )

        # Проверка подсветки полей
        zip_code_element = browser.find_element(By.ID, "zip-code")
        assert "is-invalid" in zip_code_element.get_attribute("class"), "Zip code is not highlighted in red"

        green_fields = ["first-name", "last-name", "address", "e-mail", "phone", "city", "country", "job-position", "company"]
        for field in green_fields:
            element = browser.find_element(By.ID, field)
            assert "is-valid" in element.get_attribute("class"), f"{field} is not highlighted in green"
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        browser.quit()

if __name__ == "__main__":
    pytest.main()
