from functools import cached_property
from sys import exception
from time import sleep
from browser import webdriver, By, Keys, get_browser, ActionChains, EC, drop_files
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement 
from browser import D
import os

USERNAME = os.getenv("WORKDAY_USERNAME")
PASSWORD = os.getenv("WORKDAY_PASSWORD")

CSS = By.CSS_SELECTOR
XP = By.XPATH

class ApplierError(BaseException):
    pass

def el_text_content(element, text):
    return f"//{element}[contains( text( ), '{text}')]"

def data_id_find(el, data_id, starts_with=False):
    if starts_with:
        modifier = "^"
    else:
        modifier = ""
    return (CSS, f"{el}[data-automation-id{modifier}='{data_id}']")

def find_field_by_label_content(browser, content, element="*"):
    field_id = browser.find_element(XP, el_text_content(element, content)).get_attribute("for")
    return browser.find_element(CSS, f"#{field_id}")


def text_input(browser: D, data_id, value):
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



def is_required(field):
    return bool(field.find_elements(CSS, "abbr.requiredAsterisk[title='required']"))

    
    
def how_did_you_hear_about_us(browser: D):
    section_data_id = "sourceSection"
    menu_open_data_id = "multiselectInputContainer"
    submenu_button_selector = "div[aria-label='Job Board']"
    selection_selector = "div[data-automation-label='LinkedIn.com']"
    try:
        section = browser.find_element(*data_id_find("div", section_data_id))

        section.find_element(*data_id_find("div", menu_open_data_id)).click()
        sleep(1)
        popup = browser.find_element(CSS, "div[data-automation-widget='wd-popup']")
        popup.find_element(CSS, submenu_button_selector).click()
        sleep(1)
        popup.find_element(CSS, selection_selector).click()

    except Exception as e:
        print("how_did_you_hear_about_us", e, e.args)

def have_you_ever_been_employed(browser):
    sleep(.5)
    try:
        legend = browser.find_element(XP, el_text_content("legend", "Have you ever been employed"))
        radio = legend.parent.find_element(XP, el_text_content("label", "Yes"))
        radio.click()
        radio.click()
    except Exception as e:
        print("have_you_ever_been_employed", e, e.args)



def simple_dropdown(browser, button_data_id, value):
    try:
        button = browser.find_element(*data_id_find("button", button_data_id))
        if button.text == value:
            return
        button.find_element(XP, "..").click()
        sleep(.5)
        popup = browser.find_element(CSS, "div[data-automation-widget='wd-popup']")
        popup.find_element(XP, el_text_content("div", value)).click()
    except Exception as e:
        print("simple_dropdown", button_data_id, e, e.args)


def wait_for_element(browser, by, value, timeout = 10, raise_error = False):
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
        


def delete_existing_resumes(resume_section: D):
    uploaded_items = resume_section.find_elements(*data_id_find("div", "file-upload-item"))
    for item in uploaded_items: 
        item.find_element(*data_id_find("button", "delete-file")).click()


        
def upload_resume(resume_section: D):
    resume_path = os.getcwd() + r"\BerelLevy_Resume.pdf"
    drop_zone = resume_section.find_element(*data_id_find("div", "file-upload-drop-zone"))
    drop_files(drop_zone, resume_path)


class BaseApplier:
    def __init__(
            self, 
            url: str, 
            browser: webdriver.Chrome | None = None
        ) -> None:
        """
        Base class with convenience methods.
        params:
        - browser: optional existing browser object.
        """
        self.url = url
        self.browser = browser or get_browser()
        self.action_chain = ActionChains(self.browser)

    def find_element(
            self, 
            by: str, 
            selector: str, 
            browser: D | None = None, 
            raise_error: bool = False
        ) -> WebElement | bool:
        """
        return the webelement or False if not found. option to raise error
        browser: defaults to self.browser
        """
        browser = browser or self.browser
        try:
            return self.browser.find_element(by, selector)
        except Exception as e:
            if raise_error:
                raise e
            else:
                return False
            

    def wait_for_element(
            by: str, 
            value: str, 
            browser: webdriver.Chrome | WebElement | None = None, 
            timeout = 10, 
            raise_error = False
        ):
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
            
    def find_field_by_label_content(self, content, element="*", browser: D | None = None):
        browser = browser or self.browser
        field_id = browser.find_element(XP, el_text_content(element, content)).get_attribute("for")
        return browser.find_element(CSS, f"#{field_id}")
    
    def go(self, url: str | None = None) -> None:
        self.browser.get(url or self.url)




class Applier(BaseApplier):
    

    

    
    def check_for_login(self):
        return wait_for_element(self.browser, *data_id_find("div", "signInContent"))

    def fill_login(self):
        print("login")
        text_input(self.browser, "email", USERNAME,)
        text_input(self.browser, "password", PASSWORD,)
        wait_for_element(
            self.browser,
            CSS,"div[role='button'][aria-label='Sign In']",
        ).click()

    def check_for_contact_info_page(self):
        return wait_for_element(self.browser, *data_id_find("div", "contactInformationPage"))
    
    def fill_contact_info(self):
        how_did_you_hear_about_us(self.browser)
        sleep(.5)
        have_you_ever_been_employed(self.browser)
        sleep(.5)
        simple_dropdown(self.browser, "countryDropdown", "United States of America")
        sleep(.5)
        text_input(self.browser, "legalNameSection_firstName", "Dovber")
        sleep(.5)
        text_input(self.browser, "legalNameSection_lastName", "Levy")
        sleep(.5)
        simple_dropdown(self.browser, "phone-device-type", "Mobile")
        sleep(.5)
        text_input(self.browser, "phone-number", "9176798518", )
        sleep(.5)
        self.browser.find_element(*data_id_find("button","bottom-navigation-next-button")).click()
        sleep(4)
        if wait_for_element(self.browser, *data_id_find("div", "contactInformationPage"), timeout=1):
            raise ApplierError("still on contact info page")

    def check_for_experience_page(self):
        return wait_for_element(self.browser, *data_id_find("div", "myExperiencePage"), raise_error=True)



    def fill_experience(self):
        resume_section = self.find_element(*data_id_find('div', "resumeUpload"))
        # check for existing resume
        delete_existing_resumes(resume_section)
        upload_resume(resume_section)

        self.browser.find_element(*data_id_find("button","bottom-navigation-next-button")).click()
        sleep(4)
        if wait_for_element(self.browser, *data_id_find("div", "myExperiencePage"), timeout=1):
            raise ApplierError("still on myExperiencePage")
        

    def check_for_questions_page(self):
        return wait_for_element(
            self.browser,
            *data_id_find("div", "primaryQuestionnairePage")
        )

    def fill_questions_page(self):
        pass



    def run(self):
        self.go()
        if self.check_for_login():
            sleep(.4)
            self.fill_login()
        if self.check_for_contact_info_page():
            self.fill_contact_info()
        if self.check_for_experience_page():
            self.fill_experience()





def visa(browser: D):
    find_field_by_label_content(browser, "visa", "label").click()
    popup = browser.find_element(CSS, "div[data-automation-widget='wd-popup']")
    popup.find_element(XP, el_text_content("div", "Yes")).click()

def salary(browser: D):
    find_field_by_label_content(browser, "salary", "label").click()
    popup = browser.find_element(CSS, "div[data-automation-widget='wd-popup']")
    popup.find_element(XP, el_text_content("div", "125,001 to 150,000")).click()


def education(browser: D):
    find_field_by_label_content(browser, "education", "label").click()
    popup = browser.find_element(CSS, "div[data-automation-widget='wd-popup']")
    popup.find_element(XP, el_text_content("div", "College | other")).click()


def simple_dropdown(browser, button_data_id, value):
    try:
        button = browser.find_element(*data_id_find("button", button_data_id))
        if button.text == value:
            return
        button.find_element(XP, "..").click()
        sleep(.5)
        popup = browser.find_element(CSS, "div[data-automation-widget='wd-popup']")
        popup.find_element(XP, el_text_content("div", value)).click()
    except Exception as e:
        print("simple_dropdown", button_data_id, e, e.args)



