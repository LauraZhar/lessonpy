from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def rename_button():
    browser = webdriver.Chrome()
    try:
        browser.get("http://uitestingplayground.com/textinput")
        input_field = browser.find_element(By.XPATH, "//input[@id='newButtonName']")
        input_field.send_keys("SkyPro")
        
        button = browser.find_element(By.XPATH, "//button[@id='updatingButton']")
        button.click()
        
   
        new_button_text = WebDriverWait(browser, 10).until(
            EC.text_to_be_present_in_element((By.XPATH, "//button[@id='updatingButton']"), "SkyPro")
        )
        
        print(button.text)
    finally:
        browser.quit()

rename_button()
