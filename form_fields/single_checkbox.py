from browser import XP, find_element, WebElement
from form_fields.base_form_field import BaseFormField
import xpaths


class SingleCheckBox(BaseFormField):
  XPATH = xpaths.FORM_SINGLE_CHECKBOX
  NAME_XPATH = ".//label"

  @property
  def checkbox_element(self) -> WebElement:
    return find_element(
      self.element, 
      XP, ".//input[@type='checkbox']"
    )

  @property
  def is_checked(self) -> bool:
    return self.checkbox_element.get_attribute("aria-checked") == "true"

  @property
  def answer(self):
    return self.is_checked
  
  @property
  def is_filled(self):
    return self.answer == self.correct_answer

  def fill(self):
    if self.is_filled:
      return 
    self.checkbox_element.click()
