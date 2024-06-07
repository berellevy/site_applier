from browser import (
  CSS, 
  D, 
  XP, 
  data_id_find, 
  el_text_content, 
  find_element, 
  WebElement, 
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

  def fill(self):
    if self.is_filled:
      return
    
    if self.correct_answer:
      self.open_dropdown()
      popup = find_element(
        self.element.parent, 
        CSS, "div[data-automation-widget='wd-popup']"
      )
      find_element(popup, *el_text_content("div", self.correct_answer, parent="li")).click()
    elif (not self.correct_answer) and self.is_required:
      raise KeyError(f"Input Field '{self.name}' has no correct answer.")

