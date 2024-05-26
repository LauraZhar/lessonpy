from selenium import webdriver
from selenium.webdriver.common.by import By

def click_button(browser):
    browser.get("http://the-internet.herokuapp.com/add_remove_elements/")
    add_button = browser.find_element(By.XPATH, "//button[contains(text(),'Add Element')]")
    for _ in range(5):
        add_button.click()
    delete_buttons = browser.find_elements(By.XPATH, "//button[contains(text(),'Delete')]")
    print(f"Количество кнопок 'Delete': {len(delete_buttons)}")
 
browser = webdriver.Chrome()
click_button(browser)
browser.quit()

browser = webdriver.Firefox()
click_button(browser)
browser.quit()