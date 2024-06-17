from functools import cached_property
import os
from browser import CSS, D, data_id_find, find_element, el_text_content, WebElement, Keys, xp_attr_starts_with, SELECT_ALL
from workday import is_required
from .base_form_field import BaseFormField
import xpaths


REQUIRED_FIELDS = {
  "Email Address",
  "Password",
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
    self.input_element.send_keys(SELECT_ALL)
    self.input_element.send_keys(self.correct_answer)