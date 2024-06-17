from time import sleep
from browser import (
  CSS, 
  D, 
  XP, 
  data_id_find, 
  el_text_content, 
  find_element, 
  WebElement,
  move_to_element, 
  xp_attr_starts_with
)
from form_fields.base_form_field import BaseFormField
import xpaths

class Dropdown(BaseFormField):
  XPATH = xpaths.FORM_DROPDOWN
  NAME_XPATH = ".//label"
  
  @property
  def button_element(self) -> WebElement:
    return find_element(self.element, CSS, "button[aria-haspopup]")
  
  @property
  def answer(self) -> str:
    return self.button_element.text

  @property
  def is_filled(self) -> bool:
    return self.answer == self.correct_answer
  
  @property
  def dropdown_open(self) -> bool:
    return self.button_element.get_attribute("aria-expanded") == "true"
  

  def open_dropdown(self):
    if not self.dropdown_open:
      button = find_element(self.element, CSS, "button")
      button.click()

  def _fill(self):
    move_to_element(self.element)
    sleep(.5)
    self.open_dropdown()
    popup = find_element(
      self.element.parent, 
      CSS, "div[data-automation-widget='wd-popup']"
    )
    find_element(popup, *el_text_content("div", self.correct_answer[0], parent="li"), raise_error=True).click()


