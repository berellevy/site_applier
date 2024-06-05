from functools import lru_cache
from browser import CSS, D, XP, data_id_find, el_text_content, find_element, WebElement, ActionChains, get_action_chain, move_to_element, xp_attr_starts_with
from form_fields.base_form_field import BaseFormField

CORRECT_ANSWERS = {
  "My Information.Have you worked at Etsy, Reverb, or Depop before?*": "No",
}


class Radio(BaseFormField):
  XPATH = f"""
    //div[
      {xp_attr_starts_with("data-automation-id", "formField-")}
      and .//input[@type="radio"]
    ]
  """
  NAME_XPATH = ".//legend"
  
  @property
  def correct_answer(self) -> str:
    return CORRECT_ANSWERS.get(self.name)
    

  def fill(self):
    if self.correct_answer:
      element = find_element(self.element, *el_text_content("label", self.correct_answer, parent="div"))
      move_to_element(element)
      element.click()
    elif (not self.correct_answer) and self.is_required:
      raise KeyError(f"Input Field '{self.name}' has no correct answer.")




  
