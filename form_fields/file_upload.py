

import os
from time import sleep
from typing import Literal
from drop_files import drop_files
from form_fields.base_form_field import BaseFormField
from browser import XP, d_id, find_element, WebElement, move_to_element




class MultiFileUpload(BaseFormField):
  XPATH = (
    ".//div"
    f"[{d_id('resumeSection')}]"
    f"[.//div[{d_id('file-upload-drop-zone')}]]"
  )

  NAME_XPATH = ".//h3"

  @property
  def is_required(self) -> bool:
    label_element = find_element(self.element, XP, ".//label")
    return "*" in label_element.text
  
  @property
  def uploaded_file_delete_button_elements(self) -> list[WebElement]:
    return self.element.find_elements(
      XP, 
      f".//button[{d_id('delete-file')}]"
      f"[ancestor::div[{d_id('file-upload-item')}]]"
    )
  
  def remove_uploaded_files(self):
    "recheck for the existence of delete buttons after each button click."
    move_to_element(self.element, extra_up=-200)
    while buttons:=self.uploaded_file_delete_button_elements:
      buttons[0].click()
      sleep(.2)

  @property
  def correct_answer(self) -> list[str]:
    """Return a list of absolute paths files in the resume dir in this repo"""
    folder = "resume"
    return [
      os.path.abspath(os.path.join(folder, name) )
      for name in os.listdir(folder) 
      if name != "__init__.py"
    ]
  
  def fill(self):
    self.remove_uploaded_files()
    sleep(.3)
    drop_zone_element = find_element(self.element, XP, f".//div[{d_id('file-upload-drop-zone')}]")
    drop_files(drop_zone_element, self.correct_answer)

