from utils import XP, find_element, WebElement, xpaths
from form_fields.base_form_field import BaseFormField


class SingleCheckBox(BaseFormField):
  XPATH = xpaths.FORM_SINGLE_CHECKBOX
  NAME_XPATH = ".//label[string-length(text()) > 0]"

  @property
  def checkbox_element(self) -> WebElement:
    return find_element(
      self.element, 
      ".//input[@type='checkbox']"
    )

  @property
  def is_checked(self) -> bool:
    return self.checkbox_element.get_attribute("aria-checked") == "true"

  @property
  def answer(self):
    return self.is_checked


  def _fill(self): 
    self.checkbox_element.click()
