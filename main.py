from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import time

# inp_number = input("Please input number: ")
# phone_number = "+374" + inp_number
numbers = ['95087868', '94328278', '95555229']
code = '+374'
for number in numbers:
    phone_number = code + number
    ua = UserAgent()
    user_agent = ua.random

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f'user-agent={user_agent}')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        driver.get('https://passport.yandex.ru/auth/reg/portal')
        phone_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "passp-field-phone")))
        phone_input.clear()
        phone_input.send_keys(phone_number)
        next_button = driver.find_element(By.ID, "passp:phone:controls:next")
        next_button.click()
        time.sleep(5)
        print(f"SMS sended to number {phone_number}")
    finally:
        driver.quit()
