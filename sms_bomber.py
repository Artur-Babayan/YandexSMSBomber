import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='script.log')
logger = logging.getLogger(__name__)

class YandexSMSLogin:
    def __init__(self, phone_numbers, code):
        self.phone_numbers = phone_numbers
        self.code = code
        self.ua = UserAgent()
        self.driver = None

    def setup_driver(self):
        user_agent = self.ua.random
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f'user-agent={user_agent}')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        logger.info('WebDriver initialized with user agent: %s', user_agent)

    def open_site(self, url):
        self.driver.get(url)
        logger.info('Opened site: %s', url)

    def enter_phone_number(self, phone_number):
        phone_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "passp-field-phone"))
        )
        phone_input.clear()
        phone_input.send_keys(phone_number)
        logger.info('Entered phone number: %s', phone_number)

    def click_next_button(self):
        next_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "passp:phone:controls:next"))
        )
        next_button.click()
        logger.info('Clicked "Next" button')

    def close_driver(self):
        if self.driver:
            self.driver.quit()
            logger.info('WebDriver closed')

    def run(self, url):
        for number in self.phone_numbers:
            phone_number = self.code + number
            try:
                self.setup_driver()
                self.open_site(url)
                self.enter_phone_number(phone_number)
                self.click_next_button()
                time.sleep(5)  # wait for 5 seconds after each phone number
                logger.info("SMS sent to number %s", phone_number)
            except Exception as e:
                logger.error("Error occurred for number %s: %s", phone_number, e)
            finally:
                self.close_driver()

if __name__ == "__main__":
    numbers = ['12345678', '12345678', '12345678']
    code = '+374'
    url = 'https://passport.yandex.ru/auth/reg/portal'
    yandex_sms_login = YandexSMSLogin(numbers, code)
    yandex_sms_login.run(url)
