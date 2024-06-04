"""
Searchable multi select dropdown
"""
from functools import cached_property
from time import sleep
from browser import CSS, D, data_id_find, WebElement, find_element, Keys
from .base_form_field import BaseFormField

CORRECT_ANSWERS: dict[str, list[str]] = {
  "My Information.How Did You Hear About Us?*": ["Linkedin"],
  "My Information.Country Phone Code*": ["United States of America (+1)"]

}

class MultiselectSearchField(BaseFormField):
  @cached_property
  def name(self):
    label = find_element(self.element, CSS, "label")
    return f"{self.parent_name}{label.text}"
  
  @property
  def is_required(self):
    return self.name.endswith("*")
  

  @property
  def correct_answer(self) -> str:
    return CORRECT_ANSWERS.get(self.name)

  @property
  def answers(self):
    return self.element.find_elements(*data_id_find("div", "selectedItem"))
  

  @property
  def is_filled(self):
    return {a.text for a in self.answers} == set(self.correct_answer)
  
  @property
  def dropdown_open(self) -> bool:
    return bool(find_element(self.element, *data_id_find("input", "searchBox")))
  
  def open_dropdown(self):
    if not self.dropdown_open:
      find_element(self.element, *data_id_find("div", "multiselectInputContainer")).click()


  def empty_answers(self):
    for answer in self.answers:
      find_element(answer, *data_id_find("div", "DELETE_charm")).click()
  
  
  def fill(self):
    if self.is_filled:
      return
    if self.correct_answer:
      self.empty_answers()
      self.open_dropdown()
      search_element = find_element(self.element, *data_id_find("input", "searchBox"))
      search_element.send_keys(Keys.CONTROL + "a")
      for answer in self.correct_answer:
        search_element.send_keys(answer)
        search_element.send_keys(Keys.ENTER)
    elif (not self.correct_answer) and self.is_required:
      raise KeyError(f"Input Field '{self.name}' has no correct answer.")
      



def qualify_multiselect_search_field(field: WebElement) -> bool:
  return bool(
    find_element(field, *data_id_find("div", "multiselectInputContainer"))
  )

def find_multiselect_search_fields(browser: D, parent_section=None) -> list[MultiselectSearchField]:
  inputs = browser.find_elements(*data_id_find("div", "formField", starts_with=True))
  return [MultiselectSearchField(input, parent_section) for input in inputs if qualify_multiselect_search_field(input)]