from browser import XP, find_element, WebElement
from form_fields.base_form_field import BaseFormField
import xpaths


class MonthYear(BaseFormField):
  XPATH = xpaths