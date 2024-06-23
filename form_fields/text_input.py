from utils import find_element, WebElement, SELECT_ALL, XP, xpaths
from .base_form_field import BaseFormField


REQUIRED_FIELDS = {
  "Email Address",
  "Password",
}



class TextInput(BaseFormField):
  XPATH = xpaths.FORM_TEXT_INPUT
  NAME_XPATH = ".//label"

  @property
  def is_required(self):
    return (self.name in REQUIRED_FIELDS or super().is_required)

  @property
  def input_element(self) -> WebElement:
    return find_element(self.element, ".//input")
  
  @property
  def answer(self) -> str:
    return self.input_element.get_attribute("value")


  
  def _fill(self):
    self.input_element.send_keys(SELECT_ALL)
    self.input_element.send_keys(self.correct_answer)