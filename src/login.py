from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from utils.wait_element import wait_for_element
import os
from dotenv import load_dotenv
from selenium.webdriver.support.select import Select


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

        location_container = self.driver.find_element(By.ID, "MakerComboBox")
        location_button_container = location_container.find_element(By.CLASS_NAME, "HTMLButton")
        location_select = location_button_container.find_element(By.TAG_NAME, "button")
        self.driver.execute_script("arguments[0].click();", location_select)

        select_element = self.driver.find_element(By.ID, "lookupInput")
        script = f"""
            var select = arguments[0];
            select.value = '{"PM_Cocos"}';
        """
        self.driver.execute_script(script, select_element)
        option = select_element.find_element(By.XPATH, "//option[@value='PM_Cocos']")

        actions = ActionChains(self.driver)
        actions.move_to_element(option).click().perform()