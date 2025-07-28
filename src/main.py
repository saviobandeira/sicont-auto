from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from login import LoginPage
from config import LOGIN_PAGE_URL


def create_driver(headless=False):
    options = Options()
    options.add_argument('--start-maximized')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument(f'--unsafely-treat-insecure-origin-as-secure={LOGIN_PAGE_URL}')
    if headless:
        options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)

    return driver

driver = create_driver()
LoginPage(driver).login()


print('Press any button to close.')
input()