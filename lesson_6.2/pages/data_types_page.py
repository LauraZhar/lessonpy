from selenium.webdriver.common.by import By

class DataTypesPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://bonigarcia.dev/selenium-webdriver-java/data-types.html"
        self.first_name = (By.NAME, "first-name")
        self.last_name = (By.NAME, "last-name")
        self.address = (By.NAME, "address")
        self.email = (By.NAME, "e-mail")
        self.phone = (By.NAME, "phone")
        self.zip_code = (By.ID, "zip-code")
        self.city = (By.NAME, "city")
        self.country = (By.NAME, "country")
        self.job_position = (By.NAME, "job-position")
        self.company = (By.NAME, "company")
        self.submit_button = (By.CSS_SELECTOR, "button[type='submit']")

    def load(self):
        self.driver.get(self.url)

    def fill_form(self, first_name, last_name, address, email, phone, city, country, job_position, company):
        self.driver.find_element(*self.first_name).send_keys(first_name)
        self.driver.find_element(*self.last_name).send_keys(last_name)
        self.driver.find_element(*self.address).send_keys(address)
        self.driver.find_element(*self.email).send_keys(email)
        self.driver.find_element(*self.phone).send_keys(phone)
        self.driver.find_element(*self.city).send_keys(city)
        self.driver.find_element(*self.country).send_keys(country)
        self.driver.find_element(*self.job_position).send_keys(job_position)
        self.driver.find_element(*self.company).send_keys(company)

    def submit_form(self):
        self.driver.find_element(*self.submit_button).click()

    def get_field_class_by_id(self, field_id):
        return self.driver.find_element(By.ID, field_id).get_attribute("class")

    def get_field_class_by_name(self, field_name):
        return self.driver.find_element(By.NAME, field_name).get_attribute("class")
