from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def click_button():
    browser = webdriver.Chrome()
    try:
        browser.get("http://uitestingplayground.com/ajax")
        button = browser.find_element(By.XPATH, "//button[@class='btn btn-primary']")
        button.click()
        
  
        green_box_text = WebDriverWait(browser, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//p[@class='bg-success']"))
        ).text
        
        print(green_box_text)
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        browser.quit()

click_button()
