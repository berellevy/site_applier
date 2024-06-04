from browser import CSS, D, XP, data_id_find, el_text_content, find_element, WebElement
from form_fields.base_form_field import BaseFormField

CORRECT_ANSWERS: dict[str, str] = {
  'My Information.Country*': "United States of America",
  "My Information.State*": "New York",
  "My Information.Phone Device Type*": "Mobile",
}

class Dropdown(BaseFormField):
  @property
  def name(self):
    label = find_element(self.element, CSS, "label")
    return f"{self.parent_name}{label.text}"
  
  @property
  def is_required(self):
    return "*" in self.name
  
  @property
  def button_element(self) -> WebElement:
    return find_element(self.element, CSS, "button[aria-haspopup]")
  
  @property
  def correct_answer(self) -> str:
    return CORRECT_ANSWERS.get(self.name)
  
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



def qualify_dropdown(element: WebElement):
  return bool(
    find_element(element, CSS, "button[aria-haspopup='listbox']")
  )



def find_dropdowns(browser: D, parent_section=None):
  inputs = browser.find_elements(*data_id_find("div", "formField", starts_with=True))
  return [Dropdown(input, parent_section) for input in inputs if qualify_dropdown(input)]
