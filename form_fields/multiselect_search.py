"""
Searchable multi select dropdown
"""
from functools import cached_property
from time import sleep
from browser import CSS, D, SELECT_ALL, XP, data_id_find, WebElement, find_element, Keys, move_to_element, wait_for_element, xp_attr_starts_with
from .base_form_field import BaseFormField
import xpaths


class MultiselectSearchField(BaseFormField):
  XPATH = xpaths.FORM_MULTISELECT_SEARCH
  NAME_XPATH = ".//label"

  @property
  def answer(self) -> list:
    return [a.text for a in self.answer_elements]
  

  @property
  def answer_elements(self) -> list:
    return self.element.find_elements(*data_id_find("div", "selectedItem"))


  @property
  def is_filled(self):
    return bool(
      self.correct_answer and 
      set(self.answer) == set(self.correct_answer)
    )

  @property
  def dropdown_element(self) -> WebElement:
    return find_element(self.element.parent, XP, ".//div[@data-automation-widget='wd-popup']")


  @property
  def dropdown_open(self) -> bool:
    return bool(find_element(self.element, *data_id_find("input", "searchBox")))
  
  def open_dropdown(self):
    if not self.dropdown_open:
      el = find_element(self.element, *data_id_find("div", "multiselectInputContainer"))
      move_to_element(el, extra_up=-200)
      el.click()
  
  def remove_answers(self):
    while len(self.answer_elements):
      for answer_element in self.answer_elements:
        delete_button_element = find_element(answer_element, *data_id_find("div", "DELETE_charm"))
        move_to_element(self.element, extra_up=-200)
        delete_button_element.click()
        sleep(.1)


  def fill_one(self, answer: str, search_element = None):

    search_element = search_element or find_element(self.element, *data_id_find("input", "searchBox"))
    move_to_element(search_element, extra_up=-200)
    search_element.send_keys(SELECT_ALL)
    search_element.send_keys(answer)
    search_element.send_keys(Keys.ENTER)
    choice_element = wait_for_element(self.dropdown_element, XP, f".//div[@aria-label='{answer}']", timeout=3)

    if choice_element and (not find_element(choice_element, XP, ".//div[@data-automation-checked='Checked']")):
      move_to_element(choice_element, extra_up=-200)
      choice_element.click()
    sleep(.1)
    
  
  
  def _fill(self):
    self.remove_answers()
    self.open_dropdown()
    search_element = find_element(self.element, *data_id_find("input", "searchBox"))
    for answer in self.correct_answer:
      self.fill_one(answer, search_element)
      sleep(.5)
    move_to_element(search_element, extra_up=-200)
    search_element.click()
