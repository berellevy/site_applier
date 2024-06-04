from functools import cached_property
import os
from browser import CSS, D, data_id_find, find_element, el_text_content, WebElement, Keys
from workday import is_required
from .base_form_field import BaseFormField


REQUIRED_FIELDS = {
  "Email Address",
  "Password",
}


CORRECT_ANSWERS = {
  "Email Address": os.getenv("WORKDAY_USERNAME"),
  "Password": os.getenv("WORKDAY_PASSWORD"),
  "My Information.First Name*": "Dovber",
  "My Information.Last Name*": "Levy",
  "My Information.Address Line 1*": "575 East New York Ave",
  "My Information.City*": "Brooklyn",
  "My Information.Postal Code*": "11225",
  "My Information.Phone Number*": os.getenv("PHONE_NUMBER"),
}

class TextInput(BaseFormField):

  @cached_property
  def _label(self) -> WebElement:
    return find_element(self.element, CSS, "label")
  
  @property
  def name(self) -> str:
    """Used to identify the correct answer."""
    parent_name = f"{self.parent_section.name}." if self.parent_section else ""
    return f"{parent_name}{self._label.text}"
  
  @cached_property
  def input_element(self) -> WebElement:
    return find_element(self.element, CSS, "input")
  
  @property
  def is_required(self):
    return (
      self.name in REQUIRED_FIELDS or
      self.name.endswith("*")
    )

  @cached_property
  def correct_answer(self) -> str:
    return CORRECT_ANSWERS.get(self.name)
    
  @property
  def is_filled(self):
    return self.input_element.get_attribute("value") == self.correct_answer

  
  def fill(self):
    """
    First empty the field. Then fill it.
    Raise an error if the field is required and there is no correct answer.
    """
    if self.is_filled: 
      return
    if self.correct_answer:
      self.input_element.send_keys(Keys.CONTROL + "a")
      self.input_element.send_keys(self.correct_answer)
    elif (not self.correct_answer) and self.is_required:
      raise KeyError(f"Input Field '{self.name}' has no correct answer.")
    
    


def qualify_text_input(field: WebElement) -> bool:
  is_text_or_password = (
    find_element(field, CSS, "[type='text']") or find_element(field, CSS, "[type='password']")
  )
  return bool(
    is_text_or_password and 
    (not find_element(field, CSS, "[aria-haspopup]"))
  )

def find_text_inputs(browser: D, parent_section = None) -> list[TextInput]:
  inputs = browser.find_elements(*data_id_find("div", "formField", starts_with=True))
  return [TextInput(element, parent_section) for element in inputs if qualify_text_input(element)]