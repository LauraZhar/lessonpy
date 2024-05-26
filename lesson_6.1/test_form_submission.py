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
            "zip-code": "010000",
            "city": "Москва",
            "country": "Россия",
            "job-position": "QA",
            "company": "SkyPro"
        }

        for field_name, value in fields.items():
            try:
                element = WebDriverWait(browser, 40).until(
                    EC.presence_of_element_located((By.NAME, field_name))
                )
                print(f"Найден элемент: {field_name}")
                element.clear()
                element.send_keys(value)
            except Exception as e:
                print(f"Не удалось найти элемент с name {field_name}: {e}")

        # Нажатие кнопки Submit
        try:
            submit_button = WebDriverWait(browser, 40).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Submit']"))
            )
            submit_button.click()
            print("Нажата кнопка Submit")
        except Exception as e:
            print(f"Не удалось найти или нажать кнопку Submit: {e}")

        # Ожидание проверки полей
        try:
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.NAME, "zip-code"))
            )
            print("Поля проверены")
        except Exception as e:
            print(f"Не удалось проверить поля: {e}")

        # Проверка подсветки полей
        try:
            zip_code_element = browser.find_element(By.NAME, "zip-code")
            assert "is-invalid" in zip_code_element.get_attribute("class"), "Zip code is not highlighted in red"
            print("Zip code подсвечен красным")

            green_fields = ["first-name", "last-name", "address", "e-mail", "phone", "city", "country", "job-position", "company"]
            for field in green_fields:
                element = browser.find_element(By.NAME, field)
                assert "is-valid" in element.get_attribute("class"), f"{field} is not highlighted in green"
                print(f"{field} подсвечен зеленым")
        except Exception as e:
            print(f"Ошибка при проверке подсветки полей: {e}")

    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        browser.quit()

if __name__ == "__main__":
    pytest.main()
