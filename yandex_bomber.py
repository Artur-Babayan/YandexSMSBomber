######## New version #######

import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='script.log')
logger = logging.getLogger(__name__)

class Move2ArmeniaLogin:
    def __init__(self, phone_number):
        self.phone_number = "+374" + phone_number
        self.ua = UserAgent()
        self.user_agent = self.ua.random
        self.driver = None

    def setup_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f'user-agent={self.user_agent}')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        logger.info('WebDriver initialized with user agent: %s', self.user_agent)

    def open_site(self, url):
        self.driver.get(url)
        logger.info('Opened site: %s', url)

    def click_login_button(self):
        login_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.user-area.signin-area a[href='#register']"))
        )
        login_button.click()
        logger.info('Clicked login button')

    def enter_phone_number(self):
        phone_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='tel'][name='phone']"))
        )
        phone_input.clear()
        phone_input.send_keys(self.phone_number)
        logger.info('Entered phone number: %s', self.phone_number)

    def click_get_code_button(self):
        get_code_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "form#get-code .form__submit .btn"))
        )
        get_code_button.click()
        logger.info('Clicked "Get Code" button')

    def close_driver(self):
        if self.driver:
            self.driver.quit()
            logger.info('WebDriver closed')

    def run(self, url):
        try:
            self.setup_driver()
            self.open_site(url)
            self.click_login_button()
            self.enter_phone_number()
            self.click_get_code_button()
            time.sleep(5)  # wait for 5 seconds
        finally:
            self.close_driver()

if __name__ == "__main__":
    # phone_number = input("Please input number: ")
    numbers = ['12345678', '12345678']
    for phone_number in numbers:
        url = 'https://move2armenia.am/ru/aviacompanies/utair/'
        m2a_login = Move2ArmeniaLogin(phone_number)
        m2a_login.run(url)

