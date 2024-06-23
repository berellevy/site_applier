from utils import D, XP, find_element, is_stale, move_to_element
import answers



class FormFillError(BaseException):
  pass

class BaseFormField:
  XPATH: str
  NAME_XPATH: str

  @classmethod
  def find_all(cls, browser: D, parent_section, custom_xpath: str = None):
    xpath = custom_xpath or cls.XPATH
    return [cls(f, parent_section) for f in browser.find_elements(XP, xpath)]

  def __init__(self, element: D, parent_section) -> None:
    self.element = element
    self.parent_section = parent_section

  @property
  def name(self) -> str:
    return find_element(self.element, self.NAME_XPATH).text  


  @property
  def answer(self):
    pass
  
  @property
  def correct_answer(self) -> list[str | bool]:
    """
    if an exact match isn't found, it then searches for an answer whos key
    matches the beginning of the field name.
    Example: 
    The field name "Have you worked at Etsy, Reverb, or Depop before?*"
    will match the answer key "Have you worked at"
    """
    return answers.get(**self.path)

  @property
  def is_filled(self) -> bool:
    return self.answer == self.correct_answer
  
  @property
  def path(self) -> dict[str]:
    return {
      **self.parent_section.path, 
      "field_type": type(self).__name__,
      "field_name": self.name,
    }

  @property
  def path_and_current_answer(self):
    return {**self.path, "answer": self.answer}


  @property
  def is_required(self) -> bool:
    return "*" in self.name


  @property
  def parent_name(self) -> str:
    return f"{self.parent_section.name}." if self.parent_section else ""
  
  def __repr__(self) -> str:
    classname = type(self).__name__
    name = getattr(self, "name", "")
    required = 'required, ' if getattr(self, "is_required", False) else ''
    correct_answer = f", answer: {answer}" if (answer:=getattr(self, "correct_answer", False)) else ""
    return f"<{classname}: {required}{name}{correct_answer}>"

  @property 
  def missing_answer_error(self) -> KeyError:
    return KeyError(f"Input Field '{self.name}' has no correct answer.")
  

  def fill(self):
    if is_stale(self.element):
      """This handles elements that have disapeared. if they're not there we don't have to fill them."""
      return
    try:
      if self.is_filled:
        return 
      if self.correct_answer != None: # Correct answer can sometimes be `False`!
        move_to_element(self.element, extra_up=-200)
        self._fill()
      elif (not self.correct_answer) and self.is_required:
        raise self.missing_answer_error
    except Exception as e:
        raise FormFillError(self) from e
    