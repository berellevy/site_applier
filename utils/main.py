from functools import lru_cache
from numbers import Number
from time import sleep
from typing import Literal, TypeVar, Union
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

import platform

if platform.system() == "Darwin":
  SELECT_ALL = Keys.COMMAND + "a"
elif platform.system() == "Windows":
  SELECT_ALL = Keys.CONTROL + "a"

D = TypeVar("D", bound=Union[WebDriver, WebElement])


XP = By.XPATH
"""It's just a little shorter."""


def get_browser() -> webdriver.Chrome:
  return webdriver.Chrome()

@lru_cache(maxsize=4)
def get_action_chain(browser: WebDriver):
  """same browser doesn't need new action chains each time"""
  return ActionChains(browser)

def move_to_element(element: WebElement, extra_up: Number | None = None):
  """
  extra_up: extra scrolling. positive number scrolls up, negative number scrolls down.
  """
  element.parent.execute_script("arguments[0].scrollIntoView(true);", element)
  if extra_up:
    element.parent.execute_script(f"window.scrollBy(0, {extra_up})")
  sleep(.2)
  

def find_element( 
    browser: D,
    selector: str, 
    raise_error: bool = False
  ) -> WebElement | bool:
  """
  return the webelement or False if not found. option to raise error
  """
  try:
    return browser.find_element(By.XPATH, selector)
  except Exception as e:
    if raise_error:
      raise e
    else:
      return False
    

def wait_for_element(browser, value, timeout = 10, raise_error = False):
  """Convenience wrapper."""
  try:
    return (
      WebDriverWait(browser,timeout)
      .until(EC.presence_of_element_located((By.XPATH, value)))
    )
  except Exception as e:
    if raise_error:
      raise e
    else:
      return False
  




def remove_element(element: WebElement):
  element.parent.execute_script("arguments[0].remove()", element)


def is_stale(element: WebElement) -> bool:
  try:
    element.get_attribute("")
    return False
  except StaleElementReferenceException:
    return True
