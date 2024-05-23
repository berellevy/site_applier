import typing
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

from dotenv import load_dotenv

load_dotenv()


def get_browser() -> webdriver.Chrome:
    return webdriver.Chrome()




