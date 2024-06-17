from time import sleep
from browser import XP, find_element, WebElement, Keys, is_stale
from form_fields.base_form_field import BaseFormField
import xpaths


class MonthYear(BaseFormField):
  XPATH= xpaths.FORM_MONTH_YEAR
  NAME_XPATH = ".//label" 

  @property
  def month_input_element(self) -> WebElement:
    return find_element(self.element, XP, ".//input[@aria-label='Month']")

  @property
  def year_input_element(self) -> WebElement:
    return find_element(self.element, XP, ".//input[@aria-label='Year']")

  @property
  def answer(self):
    return [
      self.month_input_element.get_attribute("value").rjust(2, "0"),
      self.year_input_element.get_attribute("value"),
    ]

  def _fill(self):
    self.month_input_element.send_keys(self.correct_answer[0])
    self.year_input_element.send_keys(self.correct_answer[1])
    self.parent_section.element.click()
