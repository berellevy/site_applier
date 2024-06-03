"""
A class for each page.
"""

from browser import D, XP, el_text_content, find_element, data_id_find
from form_fields import BaseFormField, find_form_fields





class BasePage:
  def __init__(self, browser: D) -> None:
    self.browser = browser
  
  @classmethod
  def is_current(cls, browser: D):
    raise NotImplemented()
  
  @property
  def fields(self) -> BaseFormField:
    return find_form_fields(self.browser)
  
  def fill(self):
    pass

  def next_page(self):
    pass

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
  @classmethod
  def is_current(cls, browser: D) -> bool:
    if (
      find_element(browser, *data_id_find("div", "jobPostingPage")) and 
      (not find_element(browser, *el_text_content("h2", "Start Your Application")))
    ):
      return cls(browser)

  def next_page(self):
    button = find_element(self.browser, *el_text_content("a", "Apply"))
    button.click()




@register
class StartApplication(BasePage):
  """this is a little popup with a choice of how to fill out the app."""

  @classmethod
  def is_current(cls, browser: D):
    if find_element(browser, *el_text_content("h2", "Start Your Application")):
      return cls(browser)
    

  def next_page(self):
    button = find_element(self.browser, *data_id_find("a", "useMyLastApplication"))
    button.click()

  
  @property
  def fields(self) -> list[BaseFormField]:
    return find_form_fields(self.browser)
  



@register
class SignIn(BasePage):
  @classmethod
  def is_current(cls, browser: D) -> bool:
    if (
      find_element(browser, *el_text_content("h2", "Sign In")) and
      (not find_element(browser, *data_id_find("div", "errorMessage")))
    ):
      return cls(browser)
  
  
  def fill(self):
    for field in self.fields:
      if field.is_required:
        field.fill()

  def next_page(self):
    button = find_element(self.browser, *data_id_find("button", "signInSubmitButton"))
    button.find_element(XP, "..").click()
  


# @register
# class SignInWrongPassword(BasePage):
#   def is_current(self, browser: D) -> bool:
#     return bool(
#       find_element(browser, *el_text_content("h2", "Sign In")) and
#       find_element(browser, *data_id_find("div", "errorMessage"))
#     )
  
@register
class MyInformation(BasePage):
  @classmethod
  def is_current(cls, browser: D):
    if find_element(browser, *el_text_content("h2", "My Information")):
      return cls(browser)
  
  def fill(self):
    for field in self.fields:
      if field.is_required:
        field.fill()



@register
class Unknown(BasePage):
  @classmethod
  def is_current(cls, browser: D) -> bool:
    return cls(browser)