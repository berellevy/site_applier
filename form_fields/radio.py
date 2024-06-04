from browser import CSS, D, data_id_find, el_text_content, find_element
from form_fields.base_form_field import BaseFormField

CORRECT_ANSWERS = {
  "My Information.Have you worked at Etsy, Reverb, or Depop before?*": "No",
}


class Radio(BaseFormField):
  @property
  def name(self) -> str:
    legend_text = find_element(self.element, CSS, "legend").text
    return f"{self.parent_name}{legend_text}"
  
  @property
  def is_required(self):
    return "*" in self.name
  
  @property
  def correct_answer(self) -> str:
    return CORRECT_ANSWERS.get(self.name)
    

  def fill(self):
    if self.correct_answer:
      find_element(self.element, *el_text_content("label", self.correct_answer, parent="div")).click()
    elif (not self.correct_answer) and self.is_required:
      raise KeyError(f"Input Field '{self.name}' has no correct answer.")

  @property
  def answer(self) -> str:
    return self.element


def qualify_radio(element) -> bool:
  return bool(
    find_element(element, CSS, "input[type='radio']")
  )

def find_radios(browser: D, parent_section=None):
  fields = browser.find_elements(*data_id_find("div", "formField", starts_with=True))
  return [Radio(field, parent_section) for field in fields if qualify_radio(field)]