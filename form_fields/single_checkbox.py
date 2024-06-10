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
  def is_filled(self) -> bool:
    return self.checkbox_element.get_attribute("aria-checked") == "true"
  
  
  def fill(self):
    if not self.is_filled:
      self.checkbox_element.click()
