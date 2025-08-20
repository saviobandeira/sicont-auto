import os

from typing import Optional
from typing import Tuple
from typing import Literal

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from dotenv import load_dotenv
load_dotenv()

def get_login_uri() -> str:
    return "http://ctp.sudoesteinformatica.com.br/webrun/open.do?action=open&sys=CTP"

def get_mainform_frame_locator() -> Tuple[Literal["xpath"], str]:
    return (
        By.XPATH,
        "//iframe[@name='mainform']",
    )

def find_element_by_locator(driver: WebDriver, locator: Tuple[str, str]) -> WebElement:
    return driver.find_element(*locator)

def switch_to_frame(driver: WebDriver, frame) -> None:
    driver.switch_to.frame(frame)

def switch_to_mainform_frame(driver: WebDriver) -> None:
    mainform_frame_locator = get_mainform_frame_locator()
    mainform_frame_element = find_element_by_locator(driver, mainform_frame_locator)
    switch_to_frame(driver, mainform_frame_element)

def get_env_or_fail(var_name: str) -> str:
    value: Optional[str] = os.getenv(var_name)
    if not value:
        raise ValueError(f"Variável de ambiente {var_name} não definida. Defina-a no ambiente ou em um arquivo .env.")
    
    return value

def get_username_locator() -> Tuple[Literal["xpath"], str]:
    return (
        By.XPATH,
        "//form[@name='WFRForm']//div[@id='lay']//div[@id='divcentral2']//div[@id='containerLogin']//div[@id='EdtLogin']//input[@name='WFRInput748632']",
    )

def send_keys_by_script(driver: WebDriver, element: WebElement, keys: str) -> None:
    driver.execute_script(
        "arguments[0].focus();arguments[0].value = arguments[1];arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
        element,
        keys,
    )

def fill_username_field(driver: WebDriver) -> None:
    username = get_env_or_fail("SICONT_USERNAME")
    username_locator = get_username_locator()
    username_element = find_element_by_locator(driver, username_locator)
    send_keys_by_script(driver, username_element, username)

def get_password_locator() -> Tuple[Literal["xpath"], str]:
    return (
        By.XPATH, 
        "//form[@name='WFRForm']//div[@id='lay']//div[@id='divcentral2']//div[@id='containerLogin']//div[@id='EdtSenha']//input[@name='WFRInput748633']",
    )

def fill_password_field(driver: WebDriver) -> None:
    password = get_env_or_fail("SICONT_PASSWORD")
    password_locator = get_password_locator()
    password_element = find_element_by_locator(driver, password_locator)
    send_keys_by_script(driver, password_element, password)

def get_location_options_button_locator() -> Tuple[Literal["xpath"], str]:
    return (
        By.XPATH,
        "//div[@id='MakerComboBox']//div[@class='HTMLButton']//button[@type='button']",
    )

def click_element_by_script(driver: WebDriver, element) -> None:
    driver.execute_script(
        "arguments[0].click();",
        element,
    )

def open_location_options(driver: WebDriver) -> None:
    location_options_button_locator = get_location_options_button_locator()
    location_options_button_element = find_element_by_locator(driver, location_options_button_locator)
    click_element_by_script(driver, location_options_button_element)

def get_location_options_locator() -> Tuple[Literal["id"], str]:
    return (
        By.ID,
        "lookupInput",
    )

def focus_in_option_by_script(driver: WebDriver, value: str) -> None:
    location_locator = get_location_options_locator()
    location_element = find_element_by_locator(driver, location_locator)
    script = f"var select = arguments[0];select.value = '{value}';"
    driver.execute_script(script, location_element)

def get_location_option_locator(value: str) -> Tuple[Literal["xpath"], str]:
    return (
        By.XPATH,
        f"//option[@value='{value}']",
    )

def get_action_chains(driver: WebDriver) -> ActionChains:
    return ActionChains(driver)

def move_to_element_by_action_chains(action_chains: ActionChains, element: WebElement) -> ActionChains:
    return action_chains.move_to_element(element)

def click_element_by_action_chains(action_chains: ActionChains) -> None:
    action_chains.click().perform()

def select_location(driver: WebDriver) -> None:
    location = get_env_or_fail("SICONT_LOCATION")

    open_location_options(driver)
    focus_in_option_by_script(driver, location)

    location_option_locator = get_location_option_locator(location)
    location_option_element = find_element_by_locator(driver, location_option_locator)

    action_chains = get_action_chains(driver)
    move_to_element_by_action_chains(action_chains, location_option_element)
    click_element_by_action_chains(action_chains)

def get_submit_button_locator() -> Tuple[Literal["id"], str]:
    return (
        By.ID,
        "btnlogin",
    )

def form_submit(driver: WebDriver) -> None:
    submit_button_locator = get_submit_button_locator()
    submit_button_element = find_element_by_locator(driver, submit_button_locator)

    action_chains = get_action_chains(driver)
    move_to_element_by_action_chains(action_chains, submit_button_element)
    click_element_by_action_chains(action_chains)

def login(driver: WebDriver) -> None:
    driver.get(get_login_uri())

    switch_to_mainform_frame(driver)

    fill_username_field(driver)
    fill_password_field(driver)

    select_location(driver)

    form_submit(driver)