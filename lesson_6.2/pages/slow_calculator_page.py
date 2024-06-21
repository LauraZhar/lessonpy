from selenium.webdriver.common.by import By

class SlowCalculatorPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html"
        self.delay_input = (By.ID, "delay")
        self.button_7 = (By.XPATH, "//span[text()='7']")
        self.button_plus = (By.XPATH, "//span[text()='+']")
        self.button_8 = (By.XPATH, "//span[text()='8']")
        self.button_equals = (By.XPATH, "//span[text()='=']")
        self.result = (By.XPATH, "//div[@class='screen']")

    def load(self):
        self.driver.get(self.url)

    def set_delay(self, delay):
        self.driver.find_element(*self.delay_input).clear()
        self.driver.find_element(*self.delay_input).send_keys(delay)

    def perform_calculation(self):
        self.driver.find_element(*self.button_7).click()
        self.driver.find_element(*self.button_plus).click()
        self.driver.find_element(*self.button_8).click()
        self.driver.find_element(*self.button_equals).click()

    def get_result_text(self):
        return self.driver.find_element(*self.result).text