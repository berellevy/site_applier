from time import sleep
from browser import webdriver, By, Keys
import os

USERNAME = os.getenv("WORKDAY_USERNAME")
PASSWORD = os.getenv("WORKDAY_PASSWORD")

CSS = By.CSS_SELECTOR
XP = By.XPATH

def el_text_content(element, text):
    return f"//{element}[contains( text( ), '{text}')]"

def text_input(browser, data_id, value):
    try:
        input = browser.find_element(CSS, f"input[data-automation-id='{data_id}']")
        input.send_keys(Keys.CONTROL + "a")
        input.send_keys(value)
    except Exception as e:
        print(data_id, e, e.args)

def click_button(
    element: webdriver.Chrome,
    by,
    by_value
):
    try:
        element.find_element(by, by_value).click()
    except Exception as e:
        print(by, by_value, e)
    
    
def how_did_you_hear_about_us(browser: webdriver.Chrome):
    try:
        section = browser.find_element(CSS, "div[data-automation-id='sourceSection']")
        section.find_element(CSS, "span[data-automation-id='promptIcon']").click()
        sleep(1)
        popup = browser.find_element(CSS, "div[data-automation-widget='wd-popup']")
        popup.find_element(CSS, "div[aria-label='Job Board']").click()
        sleep(1)
        popup.find_element(CSS, "div[data-automation-label='LinkedIn.com']").click()

    except Exception as e:
        print("how_did_you_hear_about_us", e, e.args)

def have_you_ever_been_employed(browser):
    try:
        legend = browser.find_element(XP, el_text_content("legend", "Have you ever been employed"))
        legend.parent.find_element(XP, el_text_content("label", "Yes")).click()
    except Exception as e:
        print("have_you_ever_been_employed", e, e.args)



def simple_dropdown(browser, button_data_id, value):
    try:
        browser.find_element(CSS, f"button[data-automation-id='{button_data_id}']").click()
        sleep(.5)
        popup = browser.find_element(CSS, "div[data-automation-widget='wd-popup']")
        popup.find_element(XP, el_text_content("div", value)).click()
    except Exception as e:
        print("simple_dropdown", button_data_id, e, e.args)
    


def apply(link: str, browser, action_chain):
    browser.get(link)
    # LOGIN
    sleep(3)
    text_input(browser, "email", USERNAME,)
    text_input(browser, "password", PASSWORD,)
    sleep(.5)
    click_button(browser, CSS, "div[data-automation-id='click_filter']")


    how_did_you_hear_about_us(browser)
    have_you_ever_been_employed(browser)
    simple_dropdown(browser, "countryDropdown", "United States of America")

    text_input(browser, "legalNameSection_firstName", "Dovber", )
    text_input(browser, "legalNameSection_lastName", "Levy", )

    text_input(browser, "addressSection_addressLine1", "575 East ny", )
    text_input(browser, "addressSection_city", "brooklyn", )
    simple_dropdown(browser, "addressSection_countryRegion", "New York")
    text_input(browser, "addressSection_postalCode", "11225", )
    text_input(browser, "phone-number", "9176798518", )


    return browser



