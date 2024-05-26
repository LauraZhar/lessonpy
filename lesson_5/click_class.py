from selenium import webdriver
from selenium.webdriver.common.by import By

def click_button_class(browser):
    browser.get("http://uitestingplayground.com/classattr")
    button = browser.find_element(By.XPATH, "//button[contains(@class, 'btn-primary')]")
    button.click()

 
browser = webdriver.Chrome()
click_button_class(browser)
browser.quit()


browser = webdriver.Firefox()
click_button_class(browser)
browser.quit()