import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.data_types_page import DataTypesPage

@pytest.fixture
def driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    yield driver
    driver.quit()

def test_form_submission(driver):
    page = DataTypesPage(driver)
    page.load()
    page.fill_form(
        first_name="Иван",
        last_name="Петров",
        address="Ленина, 55-3",
        email="test@skypro.com",
        phone="+7985899998787",
        city="Москва",
        country="Россия",
        job_position="QA",
        company="SkyPro"
    )
    page.submit_form()
    
    # Проверка, что поле Zip code подсвечено красным
    assert "alert-danger" in page.get_field_class_by_id("zip-code"), "Zip code field is not highlighted red"

    # Поля для проверки (по имени)
    fields_to_check = [
        "first-name", "last-name", "address", "e-mail", "phone", 
        "city", "country", "job-position", "company"
    ]
    for field_name in fields_to_check:
        assert "alert-success" in page.get_field_class_by_id(field_name), f"Field {field_name} is not highlighted green"
