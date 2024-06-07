from functools import lru_cache
from browser import CSS, D, XP, data_id_find, el_text_content, find_element, WebElement, ActionChains, get_action_chain, move_to_element, xp_attr_starts_with
from form_fields.base_form_field import BaseFormField
import xpaths



class Radio(BaseFormField):
  XPATH = xpaths.FORM_RADIO
  NAME_XPATH = ".//legend"
    

  def fill(self):
    if self.correct_answer:
      element = find_element(self.element, *el_text_content("label", self.correct_answer, parent="div"))
      move_to_element(element)
      element.click()
    elif (not self.correct_answer) and self.is_required:
      raise KeyError(f"Input Field '{self.name}' has no correct answer.")




  
