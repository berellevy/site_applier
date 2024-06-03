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




