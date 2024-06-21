from selenium.webdriver.common.by import By

class SwagLabsPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://www.saucedemo.com/"
        self.username = (By.ID, "user-name")
        self.password = (By.ID, "password")
        self.login_button = (By.ID, "login-button")
        self.product_1 = (By.ID, "add-to-cart-sauce-labs-backpack")
        self.product_2 = (By.ID, "add-to-cart-sauce-labs-bolt-t-shirt")
        self.product_3 = (By.ID, "add-to-cart-sauce-labs-onesie")
        self.cart_button = (By.ID, "shopping_cart_container")
        self.checkout_button = (By.ID, "checkout")
        self.first_name = (By.ID, "first-name")
        self.last_name = (By.ID, "last-name")
        self.postal_code = (By.ID, "postal-code")
        self.continue_button = (By.ID, "continue")
        self.total_label = (By.CLASS_NAME, "summary_total_label")

    def load(self):
        self.driver.get(self.url)

    def login(self, username, password):
        self.driver.find_element(*self.username).send_keys(username)
        self.driver.find_element(*self.password).send_keys(password)
        self.driver.find_element(*self.login_button).click()

    def add_products_to_cart(self):
        self.driver.find_element(*self.product_1).click()
        self.driver.find_element(*self.product_2).click()
        self.driver.find_element(*self.product_3).click()

    def proceed_to_checkout(self):
        self.driver.find_element(*self.cart_button).click()
        self.driver.find_element(*self.checkout_button).click()

    def fill_checkout_form(self, first_name, last_name, postal_code):
        self.driver.find_element(*self.first_name).send_keys(first_name)
        self.driver.find_element(*self.last_name).send_keys(last_name)
        self.driver.find_element(*self.postal_code).send_keys(postal_code)
        self.driver.find_element(*self.continue_button).click()

    def get_total(self):
        return self.driver.find_element(*self.total_label).text