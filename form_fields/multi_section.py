from browser import CSS, D, data_id_find, find_element, WebElement
from form_fields.base_form_field import BaseFormField
from form_fields.text_input import find_text_inputs


class SubSection(BaseFormField):
  @property
  def name(self):
    h4_text = find_element(self.element, CSS, "h4").text
    return f"{self.parent_name}{h4_text}"
  
  @property
  def delete_button_element(self) -> WebElement:
    return find_element(self.element, *data_id_find("button", "panel-set-delete-button"))
  
  def delete(self):
    if button:=self.delete_button_element:
      button.click()

  @property
  def form_fields(self) ->list[BaseFormField]:
    fields = []
    fields += find_text_inputs(self.element, self)
    return fields
      
  
  @property
  def is_required(self) -> bool:
    return not bool(self.delete_button_element)
  



class MultiSection(BaseFormField):
  @property
  def name(self) -> str:
    h3_text = find_element(self.element, CSS, "h3").text
    return f"{self.parent_name}{h3_text}"
  
  @property
  def add_button_element(self) -> WebElement:
    return find_element(self.element, *data_id_find("button", "Add", starts_with=True))
  
  @property
  def section_data_id(self) -> str:
    return self.element.get_attribute("data-automation-id").removesuffix("Section")

  @property
  def sub_sections(self) -> list[SubSection]:
    data_id = data_id_find("div", f"{self.section_data_id}-", starts_with=True)
    elements = self.element.find_elements(*data_id)
    return [SubSection(e, self) for e in elements]





def qualify_multi_section(element: D) -> D:
  return bool(find_element(element, *data_id_find("button", "Add", starts_with=True)))

def find_multi_sections(browser: D, parent_section = None) -> list[MultiSection]:
  sections = browser.find_elements(*data_id_find("div", "Section", ends_with=True))
  return [MultiSection(section, parent_section) for section in sections if qualify_multi_section(section)]