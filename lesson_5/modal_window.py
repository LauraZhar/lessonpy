from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def handle_modal_window(browser):
    browser.get("http://the-internet.herokuapp.com/entry_ad")
    try:
        close_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='modal-footer']/p"))
        )
        close_button.click()
    except Exception as e:
        print(f"Ошибка: {e}")

 
browser = webdriver.Chrome()
handle_modal_window(browser)
browser.quit()