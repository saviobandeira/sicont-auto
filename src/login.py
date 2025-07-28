from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from utils.wait_element import wait_for_element
import os
from dotenv import load_dotenv


load_dotenv()

class LoginPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.username = os.getenv("SICONT_USERNAME")
        self.password = os.getenv("SICONT_PASSWORD")

    def login(self):
        self.driver.get("http://ctp.sudoesteinformatica.com.br/webrun/open.do?action=open&sys=CTP")

        iframe_locator = (By.XPATH, "//iframe[@name='mainform']")
        iframe = wait_for_element(self.driver, iframe_locator)
        self.driver.switch_to.frame(iframe)

        username_field = self.driver.find_element(By.XPATH, """
                //form[@name='WFRForm']
                //div[@id='lay']
                //div[@id='divcentral2']
                //div[@id='containerLogin']
                //div[@id='EdtLogin']
                //input[@name='WFRInput748632']
            """
        )
        username_field.send_keys(self.username)

        password_field = self.driver.find_element(By.XPATH, """
                //form[@name='WFRForm']
                //div[@id='lay']
                //div[@id='divcentral2']
                //div[@id='containerLogin']
                //div[@id='EdtSenha']
                //input[@name='WFRInput748633']
            """
        )
        self.driver.execute_script("""
                arguments[0].focus();
                arguments[0].value = arguments[1];
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            """,
            password_field,
            self.password
        )

        # login_button_locator = (By.ID, 'btnlogin')
        # print("Bucando o botão de login")
        # self.driver.find_element(*login_button_locator).submit()
        