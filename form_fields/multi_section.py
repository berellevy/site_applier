from time import sleep
from utils import D, XP, find_element, WebElement, move_to_element, d_id, xpaths
from form_fields.base_form_field import BaseFormField
from form_fields.dropdown import Dropdown
from form_fields.single_checkbox import SingleCheckBox
from form_fields.text_input import TextInput
from form_fields.month_year import MonthYear
from form_fields.text_area import TextArea
import answers


class RequiredError(BaseException):
  pass


class SubSection(BaseFormField):
  NAME_XPATH = ".//h4"

  @property
  def ANSWERS(self):
    return self.correct_answer

  @classmethod
  def find_all(cls, browser: D, parent_section):
    xpath = (
      ".//div"
      f"[{d_id(parent_section.section_data_id, 'startswith')}]"
    )
    return [cls(f, parent_section) for f in browser.find_elements(XP, xpath)]
  
  @property
  def path(self) -> dict[str]:
    return {**self.parent_section.path, "sub_section": self.name}


  @property
  def delete_button_element(self) -> WebElement:
    return find_element(self.element, f".//button[{d_id('panel-set-delete-button')}]")
  
  def delete(self):
    if button:=self.delete_button_element:
      move_to_element(button)
      button.click()
      sleep(.5)
    else:
      raise RequiredError(self.path)

  def xpath_customizer(self, xpath: str) -> str:
    return xpath.removesuffix(xpaths.MULTISECTION_EXCLUDER)
  
  def find_all_override(self, input: BaseFormField) -> list[BaseFormField]:
    """remove the multisection excluder xpath snippet from the form_fields `XPATH` property"""
    custom_xpath = input.XPATH.removesuffix(xpaths.MULTISECTION_EXCLUDER)
    return input.find_all(self.element, self, custom_xpath)

  @property
  def form_fields(self) ->list[BaseFormField]:
    return [
      *self.find_all_override(SingleCheckBox),
      *self.find_all_override(TextInput),
      *self.find_all_override(Dropdown),
      *self.find_all_override(TextArea),
      *self.find_all_override(MonthYear),
    ]

  @property
  def answer(self):
    return {
      field.name: field.answer 
      for field in self.form_fields
    }
      
  
  @property
  def is_required(self) -> bool:
    return not bool(self.delete_button_element)
  

  def fill(self):
    for field in self.form_fields:
      field.fill()
  

 

class MultiSection(BaseFormField):
  XPATH = xpaths.FORM_MULTISECTION
  NAME_XPATH = ".//h3"

  @property
  def path(self) -> dict[str]:
    return {**self.parent_section.path, "section": self.name}
  
  @property
  def add_button_element(self) -> WebElement:
    return find_element(self.element, f".//button[{d_id('Add', 'startswith')}]")
  
  def add_subsection(self):
    button = self.add_button_element
    move_to_element(button)
    button.click()
  
  @property
  def section_data_id(self) -> str:
    """used in the subsections xpath"""
    return self.element.get_attribute("data-automation-id").removesuffix("Section")
  
  
  @property
  def existing_sub_sections(self) -> list[SubSection]:
    return SubSection.find_all(self.element, self)
  
  @property
  def correct_answer(self):
    """The names of the subsections that we have answers for."""
    return answers.get_sub_sections(**self.path)
  
  @property
  def correct_sub_sections(self):
    """
    - remove non required subsections
    - add required subsections if missing (using len of correct answer)
    """
    # REMOVE UNREQUIRED SUBSECTIONS
    required_subsections = [*self.correct_answer]
    for sub_section in self.existing_sub_sections:
      if not (sub_section.name in required_subsections):
        sub_section.delete()
    # ADD REQUIRED SUBSECTIONS
    while len(self.existing_sub_sections)<len(required_subsections):
      self.add_subsection()
      sleep(.3)
    return self.existing_sub_sections
    
  def _fill(self):
    for sub_section in self.correct_sub_sections:
      sub_section.fill()
      
    
  

  
  


  


