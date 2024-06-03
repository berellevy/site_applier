

from browser import CSS, D, data_id_find, find_element, WebElement
from form_fields.base_form_field import BaseFormField

class Dropdown(BaseFormField):
  @property
  def name(self):
    label = find_element(self.element, CSS, "label")
    return label.text
  
  @property
  def is_required(self):
    return "*" in self.name


def qualify_dropdown(element: WebElement):
  return bool(
    find_element(element, CSS, "button[aria-haspopup='listbox']")
  )

def find_dropdowns(browser: D):
  inputs = browser.find_elements(*data_id_find("div", "formField", starts_with=True))
  return [Dropdown(input) for input in inputs if qualify_dropdown(input)]
