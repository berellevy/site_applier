from functools import cached_property
import os
from browser import CSS, D, data_id_find, find_element, el_text_content, WebElement, Keys, xp_attr_starts_with
from workday import is_required
from .base_form_field import BaseFormField


REQUIRED_FIELDS = {
  "Sign In.Email Address",
  "Sign In.Password",
}


CORRECT_ANSWERS = {
  "Sign In.Email Address": os.getenv("WORKDAY_USERNAME"),
  "Sign In.Password": os.getenv("WORKDAY_PASSWORD"),
  "My Information.First Name*": "Dovber",
  "My Information.Last Name*": "Levy",
  "My Information.Address Line 1*": "575 East New York Ave",
  "My Information.City*": "Brooklyn",
  "My Information.Postal Code*": "11225",
  "My Information.Phone Number*": os.getenv("PHONE_NUMBER"),
}

class TextInput(BaseFormField):
  XPATH = f"""
    //div
    [{xp_attr_starts_with("data-automation-id", "formField-")}]
    [.//input[@type="text"] or .//input[@type="password"]]
    [not(.//*[@aria-haspopup])]
  """
  NAME_XPATH = ".//label"
  
  @cached_property
  def input_element(self) -> WebElement:
    return find_element(self.element, CSS, "input")
  
  @property
  def is_required(self):
    return (
      self.name in REQUIRED_FIELDS or super().is_required
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
    