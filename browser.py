from functools import lru_cache
from numbers import Number
from time import sleep
from typing import Literal, TypeVar, Union
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

import platform

if platform.system() == "Darwin":
  SELECT_ALL = Keys.COMMAND + "a"
elif platform.system() == "Windows":
  SELECT_ALL = Keys.CONTROL + "a"

D = TypeVar("D", bound=Union[WebDriver, WebElement])

from drop_files import drop_files

from dotenv import load_dotenv

load_dotenv()

CSS = By.CSS_SELECTOR
XP = By.XPATH


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
    

def wait_for_element(browser, by, value, timeout = 10, raise_error = False):
  """Convenience wrapper."""
  try:
    return (
      WebDriverWait(browser,timeout,)
      .until(EC.presence_of_element_located((by, value)))
    )
  except Exception as e:
    if raise_error:
      raise e
    else:
      return False
    

def data_id_find(el, data_id, starts_with=False, ends_with=False) -> tuple[str, str]:
  if starts_with:
    modifier = "^"
  elif ends_with:
    modifier = "$"
  else:
    modifier = ""
  return (CSS, f"{el}[data-automation-id{modifier}='{data_id}']")


def el_text_content(
  element: str, 
  text: str, 
  parent: str = None
) -> tuple[str, str]:
  """
  params:
   - element: Valid html element or '*'
   - text: 
   - parent: If you want to select the parent element of the element containing the text, specify the parent element's correct tag name / identifier.
    
  """
  suffix = f"/parent::{parent}" if parent else ""
  return (XP, f"//{element}[contains( text( ), '{text}')]{suffix}")

def xp_attr_ends_with(attr: str, value: str) -> str:
  """because xpath 1. attr can also be `'text()'`"""
  if not attr == "text()":
    attr = f"@{attr}"
  return f"substring({attr}, string-length({attr}) - string-length('{value}') + 1) = '{value}'"


def xp_attr_starts_with(attr: str, value: str) -> str:
  attr = f"@{attr}" if attr != "text()" else attr
  return f"starts-with({attr}, '{value}')"

def xp_attr_contains(attr: str, value: str) -> str:
  attr = f"@{attr}" if attr != "text()" else attr
  return f"contains({attr}, '{value}')"


def remove_element(element: WebElement):
  element.parent.execute_script("arguments[0].remove()", element)


def is_stale(element: WebElement) -> bool:
  try:
    element.get_attribute("")
    return False
  except StaleElementReferenceException:
    return True
  


def d_id(value, match_type: Literal["exact", "startswith", "endswith", "contains"] = "exact") -> str:
  """
  Abbreviation for attribute data-automation-id='value'.
  
  Examples: 
  >>> d_di("hello")
  "@data-automation-id='hello'"
  >>> d_id("hello", match_type="startswith")
  "starts-with(@data-automation-id, 'hello')"
  >>> d_id("hello", match_type="endswith")
  "substring(@data-automation-id, string-length(@data-automation-id) - string-length('hello') + 1) = 'hello'"
  >>> d_id("hello", match_type="contains")
  "contains(@data-automation-id, 'hello')"
  """
  attr = "data-automation-id"
  return {
    "exact": f"@{attr}='{value}'",
    "startswith": xp_attr_starts_with(attr, value),
    "endswith": xp_attr_ends_with(attr, value),
    "contains": xp_attr_contains(attr, value)
  }[match_type]