"""
A class for each page.
"""

import os
from browser import D, XP, find_element, data_id_find, remove_element, xp_attr_starts_with
from form_fields import BaseFormField, TextInput, MultiselectSearchField, Dropdown, Radio
from form_fields.single_checkbox import SingleCheckBox
from form_fields.text_area import TextArea
from form_fields.file_upload import MultiFileUpload
from form_fields.multi_section import MultiSection
import xpaths




class BasePage:
  name: str
  XPATH: str = ""
  NEXT_PAGE_BUTTON_XPATH: str = ""
  def __init__(self, browser: D) -> None:
    self.browser = browser
  
  @classmethod
  def is_current(cls, browser: D) -> bool:
    if find_element(browser, XP, cls.XPATH):
      return cls(browser)

  @property
  def fields(self) -> BaseFormField:
    return [
      *TextInput.find_all(self.browser, self),
      *MultiselectSearchField.find_all(self.browser, self),
      *Dropdown.find_all(self.browser, self),
      *Radio.find_all(self.browser, self),
      *MultiSection.find_all(self.browser, self),
      *MultiFileUpload.find_all(self.browser, self),
      *TextArea.find_all(self.browser, self),
      *SingleCheckBox.find_all(self.browser, self),
    ]
  
  @property
  def path(self) -> list[str]:
    """Needed by form field path methods."""
    return {"page": self.name}
  
  def delete_header(self):
    """The header element sometimes blocks clicks to form fields."""
    if header:=find_element(self.browser, *data_id_find("div", "header")):
      remove_element(header)

  def fill(self):
    for field in self.fields:
      field.fill()

  def next_page(self):
    self.fill()
    find_element(self.browser, XP, self.NEXT_PAGE_BUTTON_XPATH).click()


PAGES: list[BasePage] = []

def register(page: BasePage):
  PAGES.append(page)


def get_current_page(browser: D) -> BasePage:
  for page in PAGES:
    if current_page:=page.is_current(browser):
      return current_page

@register
class JobDescription(BasePage):
  """
  just needs a next_page method since there is no filling to do.
  """
  name = "Job Description"
  XPATH = xpaths.JOB_DESCRIPTION_PAGE
  NEXT_PAGE_BUTTON_XPATH = "//a[text()='Apply']"




@register
class StartApplication(BasePage):
  """this is a little popup with a choice of how to fill out the app."""
  name = "Start Your Application"
  XPATH = xpaths.START_APPLICATION_PAGE
  NEXT_PAGE_BUTTON_XPATH = "//a[@data-automation-id='useMyLastApplication']"
  



@register
class SignIn(BasePage):
  name = "Sign In"
  XPATH = xpaths.SIGN_IN_PAGE
  NEXT_PAGE_BUTTON_XPATH = """
  //button[@data-automation-id='signInSubmitButton']/parent::div
  """
  ANSWERS = {
    TextInput: {
      "Email Address": os.getenv("WORKDAY_USERNAME"),
      "Password": os.getenv("WORKDAY_PASSWORD"),
    },
  }
  
  
@register
class MyInformation(BasePage):
  name = "My Information"
  XPATH = xpaths.MY_INFORMATION_PAGE
  NEXT_PAGE_BUTTON_XPATH = "//button[@data-automation-id='bottom-navigation-next-button']"
  ANSWERS = {
    TextInput: {
      "First Name*": "Dovber",
      "Last Name*": "Levy",
      "Address Line 1*": "575 East New York Ave",
      "City*": "Brooklyn",
      "Postal Code*": "11225",
      "Phone Number*": os.getenv("PHONE_NUMBER"),
    },
    MultiselectSearchField: {
        "How Did You Hear About Us?*": ["Linkedin"],
        "Country Phone Code*": ["United States of America (+1)"],
    },
    Dropdown: {
      "Country*": "United States of America",
      "State*": "New York",
      "Phone Device Type*": "Mobile",
    },
    Radio: {
      "Have you worked at": "No",
    },
  }

  def fill(self):
    self.delete_header()
    super().fill()



@register
class MyExperience(BasePage):
  name = "My Experience"
  XPATH = xpaths.MY_EXPERIENCE_PAGE
  NEXT_PAGE_BUTTON_XPATH = "//button[@data-automation-id='bottom-navigation-next-button']"
    
@register
class ApplicationQuestions(BasePage):
  name = "Application Questions"
  XPATH = f"//h2[{xp_attr_starts_with('text()', 'Application Questions')}]"
  NEXT_PAGE_BUTTON_XPATH = "//button[@data-automation-id='bottom-navigation-next-button']"

@register
class VoluntaryDisclosures(BasePage):
  name = "Voluntary Disclosures"
  XPATH = f"//h2[{xp_attr_starts_with('text()', 'Voluntary Disclosures')}]"
  NEXT_PAGE_BUTTON_XPATH = "//button[@data-automation-id='bottom-navigation-next-button']"


@register
class Unknown(BasePage):
  name = "Unknown"
  @classmethod
  def is_current(cls, browser: D) -> bool:
    """will always return the browser"""
    return cls(browser)