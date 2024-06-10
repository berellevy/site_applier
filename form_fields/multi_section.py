from browser import CSS, D, XP, data_id_find, find_element, WebElement, xp_attr_ends_with, xp_attr_starts_with
from form_fields.base_form_field import BaseFormField
from form_fields.dropdown import Dropdown
from form_fields.single_checkbox import SingleCheckBox
from form_fields.text_input import TextInput
import xpaths





class SubSection(BaseFormField):
  NAME_XPATH = ".//h4"

  @property
  def ANSWERS(self):
    return self.correct_answer

  @classmethod
  def find_all(cls, browser: D, parent_section):
    xpath = f"""
      .//div
      [{xp_attr_starts_with("data-automation-id", parent_section.section_data_id)}]
    """
    return [cls(f, parent_section) for f in browser.find_elements(XP, xpath)]
  
  @property
  def delete_button_element(self) -> WebElement:
    return find_element(self.element, *data_id_find("button", "panel-set-delete-button"))
  
  def delete(self):
    if button:=self.delete_button_element:
      button.click()

  def xpath_customizer(self, xpath: str) -> str:
    return xpath.removesuffix(xpaths.MULTISECTION_EXCLUDER)
  
  def find_all_override(self, input: BaseFormField) -> list[BaseFormField]:
    custom_xpath = input.XPATH.removesuffix(xpaths.MULTISECTION_EXCLUDER)
    return input.find_all(self.element, self, custom_xpath)

  @property
  def form_fields(self) ->list[BaseFormField]:
    return [
      *self.find_all_override(SingleCheckBox),
      *self.find_all_override(TextInput),
      *self.find_all_override(Dropdown),
    ]
      
  
  @property
  def is_required(self) -> bool:
    return not bool(self.delete_button_element)
  

 

class MultiSection(BaseFormField):
  XPATH = xpaths.FORM_MULTISECTION
  NAME_XPATH = ".//h3"

  
  
  @property
  def add_button_element(self) -> WebElement:
    return find_element(self.element, *data_id_find("button", "Add", starts_with=True))
  
  @property
  def section_data_id(self) -> str:
    """used in the subsections xpath"""
    return self.element.get_attribute("data-automation-id").removesuffix("Section")

  @property
  def sub_sections(self) -> list[SubSection]:
    return SubSection.find_all(self.element, self)
  

  ANSWERS = {
    SubSection: {
      "Work Experience 1": {
        TextInput: {
          "Job Title": "Software Engineer",
          "Company": "Allin1Ship",
          "Location": "Brooklyn, NY",
        },
        SingleCheckBox: {
          "I currently work here": True,
        }
      },
      "Work Experience 2": {},
    }
  }
