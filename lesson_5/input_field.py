from selenium import webdriver
from selenium.webdriver.common.by import By

def input_text_field(browser):
    browser.get("http://the-internet.herokuapp.com/inputs")
    input_field = browser.find_element(By.XPATH, "//input[@type='number']")
    input_field.send_keys("1000")
    input_field.clear()
    input_field.send_keys("999")

 
browser = webdriver.Chrome()
input_text_field(browser)
browser.quit()