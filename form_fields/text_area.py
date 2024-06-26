from functools import cached_property
import os
from utils import find_element, WebElement, XP, SELECT_ALL, xpaths
from .base_form_field import BaseFormField


CORRECT_ANSWERS = {
  
}

class TextArea(BaseFormField):
  XPATH = xpaths.FORM_TEXT_AREA
  NAME_XPATH = ".//label"

  @cached_property
  def input_element(self) -> WebElement:
    return find_element(self.element, ".//textarea")


  @property
  def answer(self):
    return self.input_element.get_attribute("value")
    
  @property
  def is_filled(self):
    return self.answer == self.correct_answer
  
  @property
  def correct_answer(self):
    return "\n".join(super().correct_answer or [])

  
  def _fill(self):
    self.input_element.send_keys(SELECT_ALL)
    self.input_element.send_keys(self.correct_answer)
    
    