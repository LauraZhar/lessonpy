from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_for_images():
    browser = webdriver.Chrome()
    try:
        browser.get("https://bonigarcia.dev/selenium-webdriver-java/loading-images.html")
        
       
        WebDriverWait(browser, 30).until(
            EC.text_to_be_present_in_element((By.ID, "loading"), "Done!")
        )

 
        images = WebDriverWait(browser, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@id='image-container']/img"))
        )
        
  
        if len(images) >= 3:
            image_src = images[2].get_attribute("src")
            print(f"src третьей картинки: {image_src}")
        else:
            print("Не удалось найти третью картинку")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        browser.quit()

wait_for_images()
