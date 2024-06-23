from utils import xp, find_element, move_to_element, xpaths
from form_fields.base_form_field import BaseFormField



class Radio(BaseFormField):
  XPATH = xpaths.FORM_RADIO
  NAME_XPATH = ".//legend"
    

  def _fill(self):
    element = find_element(self.element, f".//div[label[{xp.attr_contains("text()", self.correct_answer)}]]")
    move_to_element(element)
    element.click()



  
