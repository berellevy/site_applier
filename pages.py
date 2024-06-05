"""
A class for each page.
"""

from browser import D, XP, el_text_content, find_element, data_id_find, remove_element, xp_attr_starts_with
from form_fields import BaseFormField, TextInput, MultiselectSearchField, Dropdown, Radio





class BasePage:
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
    ]
  
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
  XPATH = """
  //body[
    .//div[@data-automation-id="jobPostingPage"] 
    and not(.//h2[contains(text(),"Start Your Application")])
  ]
  """
  NEXT_PAGE_BUTTON_XPATH = """
  //a[text()="Apply"]
  """




@register
class StartApplication(BasePage):
  """this is a little popup with a choice of how to fill out the app."""
  name = "Start Your Application"
  XPATH = """
  //body[
    .//div[@data-automation-id="jobPostingPage"] 
    and .//h2[contains(text(),"Start Your Application")]
  ]
  """
  NEXT_PAGE_BUTTON_XPATH = "//a[@data-automation-id='useMyLastApplication']"
  



@register
class SignIn(BasePage):
  name = "Sign In"
  XPATH = """
  //div[
    @id='mainContent' and 
    .//h2[text()='Sign In'] 
    and not(.//div[@data-automation-id='errorMessage'])]
  """
  NEXT_PAGE_BUTTON_XPATH = """
  //button[@data-automation-id="signInSubmitButton"]/parent::div
  """
  
  
@register
class MyInformation(BasePage):
  name = "My Information"
  XPATH = f"//h2[{xp_attr_starts_with('text()', 'My Information')}]"
  NEXT_PAGE_BUTTON_XPATH = "//button[@data-automation-id='bottom-navigation-next-button']"
  
  def fill(self):
    self.delete_header()
    super().fill()



@register
class MyExperience(BasePage):
  name = "My Experience"
  XPATH = f"//h2[{xp_attr_starts_with('text()', 'My Experience')}]"
    



@register
class Unknown(BasePage):
  @classmethod
  def is_current(cls, browser: D) -> bool:
    """will always return the browser"""
    return cls(browser)