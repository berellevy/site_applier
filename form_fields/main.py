from .single_checkbox import SingleCheckBox
from .text_area import TextArea
from .dropdown import Dropdown
from .multiselect_search import MultiselectSearchField
from .radio import Radio
from .text_input import TextInput
from .base_form_field import BaseFormField
from .multi_section import MultiSection
from .file_upload import MultiFileUpload

def get_fields(page) -> BaseFormField:
  return [
    *TextInput.find_all(page.browser, page),
    *MultiselectSearchField.find_all(page.browser, page),
    *Dropdown.find_all(page.browser, page),
    *Radio.find_all(page.browser, page),
    *MultiSection.find_all(page.browser, page),
    *MultiFileUpload.find_all(page.browser, page),
    *TextArea.find_all(page.browser, page),
    *SingleCheckBox.find_all(page.browser, page),
  ]