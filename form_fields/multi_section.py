from browser import CSS, D, XP, data_id_find, find_element, WebElement, xp_attr_ends_with, xp_attr_starts_with
from form_fields.base_form_field import BaseFormField
from form_fields.text_input import TextInput


class SubSection(BaseFormField):
  NAME_XPATH = ".//h4"

  @classmethod
  def find_all(cls, browser: D, parent_section):
    xpath = f"""
      .//div
      [{xp_attr_starts_with("data-automation-id", parent_section.section_data_id + "-")}]
    """
    return [cls(f, parent_section) for f in browser.find_elements(XP, xpath)]
  
  @property
  def delete_button_element(self) -> WebElement:
    return find_element(self.element, *data_id_find("button", "panel-set-delete-button"))
  
  def delete(self):
    if button:=self.delete_button_element:
      button.click()

  @property
  def form_fields(self) ->list[BaseFormField]:
    return [
      *TextInput.find_all(self.element, self),
    ]
      
  
  @property
  def is_required(self) -> bool:
    return not bool(self.delete_button_element)
  

 

class MultiSection(BaseFormField):
  XPATH = f"""
    //div
    [{xp_attr_ends_with('data-automation-id', 'Section')}]
    [.//button[{xp_attr_starts_with('text()', 'Add')}]]
  """
  NAME_XPATH = ".//h3"
  
  @property
  def add_button_element(self) -> WebElement:
    return find_element(self.element, *data_id_find("button", "Add", starts_with=True))
  
  @property
  def section_data_id(self) -> str:
    return self.element.get_attribute("data-automation-id").removesuffix("Section")

  @property
  def sub_sections(self) -> list[SubSection]:
    return SubSection.find_all(self.element, self)
