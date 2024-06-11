from functools import cached_property
import os
from browser import CSS, D, data_id_find, find_element, el_text_content, WebElement, Keys, xp_attr_starts_with, XP, SELECT_ALL
from workday import is_required
from .base_form_field import BaseFormField
import xpaths


CORRECT_ANSWERS = {
  
}

class TextArea(BaseFormField):
  XPATH = xpaths.FORM_TEXT_AREA
  NAME_XPATH = ".//label"

  @cached_property
  def input_element(self) -> WebElement:
    return find_element(self.element, XP, ".//textarea")
    
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
      self.input_element.send_keys(SELECT_ALL)
      self.input_element.send_keys(self.correct_answer)
    elif (not self.correct_answer) and self.is_required:
      raise self.missing_answer_error
    