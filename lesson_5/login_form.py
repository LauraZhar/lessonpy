from selenium import webdriver
from selenium.webdriver.common.by import By

def login_form(browser):
    browser.get("http://the-internet.herokuapp.com/login")
    username_field = browser.find_element(By.XPATH, "//input[@id='username']")
    password_field = browser.find_element(By.XPATH, "//input[@id='password']")
    login_button = browser.find_element(By.XPATH, "//button[@type='submit']")
    
    username_field.send_keys("tomsmith")
    password_field.send_keys("SuperSecretPassword!")
    login_button.click()

 
browser = webdriver.Chrome()
login_form(browser)
browser.quit()