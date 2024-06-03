from typing import TypeVar, Union
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

D = TypeVar("D", bound=Union[WebDriver, WebElement])

from drop_files import drop_files

from dotenv import load_dotenv

load_dotenv()

CSS = By.CSS_SELECTOR
XP = By.XPATH


def get_browser() -> webdriver.Chrome:
    return webdriver.Chrome()



def find_element( 
        browser: D,
        by: str, 
        selector: str, 
        raise_error: bool = False
    ) -> WebElement | bool:
    """
    return the webelement or False if not found. option to raise error
    """
    try:
        return browser.find_element(by, selector)
    except Exception as e:
        if raise_error:
            raise e
        else:
            return False
        

def data_id_find(el, data_id, starts_with=False):
    if starts_with:
        modifier = "^"
    else:
        modifier = ""
    return (CSS, f"{el}[data-automation-id{modifier}='{data_id}']")


def el_text_content(element, text) -> tuple[str, str]:
    return (XP, f"//{element}[contains( text( ), '{text}')]")