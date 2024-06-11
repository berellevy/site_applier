from browser import XP, find_element, WebElement, Keys
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
    return (
      find_element(self.element, XP, ".//div[@data-automation-id='dateSectionMonth-display']").text,
      find_element(self.element, XP, ".//div[@data-automation-id='dateSectionYear-display']").text,
    )

  @property
  def is_filled(self) -> bool:
    return self.answer == self.correct_answer

  def fill(self):
    if self.is_filled:
      return
    if self.correct_answer:
      self.month_input_element.send_keys(Keys.DELETE)
      self.month_input_element.send_keys(self.correct_answer[0])
      self.year_input_element.send_keys(Keys.DELETE)
      self.year_input_element.send_keys(self.correct_answer[1])
    elif self.is_required and (not self.correct_answer):
      raise self.missing_answer_error

