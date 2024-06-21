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
  def is_current(cls, browser: D, custom_xpath: str | None = None) -> bool:
    xpath = custom_xpath or cls.XPATH
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
  return page


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
  
  
@register
class MyInformation(BasePage):
  name = "My Information"
  XPATH = xpaths.MY_INFORMATION_PAGE
  NEXT_PAGE_BUTTON_XPATH = "//button[@data-automation-id='bottom-navigation-next-button']"
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
  XPATH = xpaths.APPLICATION_QUESTIONS_PAGE
  NEXT_PAGE_BUTTON_XPATH = "//button[@data-automation-id='bottom-navigation-next-button']"

@register
class VoluntaryDisclosures(BasePage):
  name = "Voluntary Disclosures"
  XPATH = xpaths.VOLUNTARY_DISCLOSURES_PAGE
  NEXT_PAGE_BUTTON_XPATH = "//button[@data-automation-id='bottom-navigation-next-button']"

@register
class Review(BasePage):
  name = "Review"
  XPATH = xpaths.REVIEW_PAGE
  NEXT_PAGE_BUTTON_XPATH = "//button[@data-automation-id='bottom-navigation-next-button']"


@register
class AlreadyApplied(BasePage):
  name = "Already Applied"
  XPATH = xpaths.ALREADY_APPLIED_PAGE
  def next_page(self):
    return "Already applied."


@register
class Unknown(BasePage):
  name = "Unknown"
  @classmethod
  def is_current(cls, browser: D) -> bool:
    """will always return the browser"""
    return cls(browser)