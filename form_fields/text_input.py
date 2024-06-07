from functools import cached_property
import os
from browser import CSS, D, data_id_find, find_element, el_text_content, WebElement, Keys, xp_attr_starts_with
from workday import is_required
from .base_form_field import BaseFormField
import xpaths


REQUIRED_FIELDS = {
  "Email Address",
  "Sign In.Password",
}


CORRECT_ANSWERS = {
  
}

class TextInput(BaseFormField):
  XPATH = xpaths.FORM_TEXT_INPUT
  NAME_XPATH = ".//label"

  @property
  def is_required(self):
    return (
      self.name in REQUIRED_FIELDS or super().is_required
    )

  @cached_property
  def input_element(self) -> WebElement:
    return find_element(self.element, CSS, "input")
  
    
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
    