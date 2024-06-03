from functools import cached_property
import os
from browser import CSS, D, data_id_find, find_element, el_text_content, WebElement, Keys
from form_fields.multiselect_search import find_multiselect_search_fields
from .text_input import find_text_inputs
from .base_form_field import BaseFormField










def find_form_fields(browser: D) -> list[BaseFormField]:
  fields = []
  fields += find_text_inputs(browser)
  fields += find_multiselect_search_fields(browser)

  return fields