from browser import D, XP, find_element

def key_is_prefix(d: dict, lookup: str):
  """
  Access a key in a dict even if the key only matches part of the lookup prefix.
  Not efficient at all. Only good for small dicts. (oh baby)
  """
  for key in (d):
    if lookup.startswith(key):
      return d[key]


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
    return find_element(self.element, XP, self.NAME_XPATH).text  


  @property
  def answer(self):
    pass
  
  @property
  def correct_answer(self) -> str:
    """
    if an exact match isn't found, it then searches for an answer whos key
    matches the beginning of the field name.
    Example: 
    The field name "Have you worked at Etsy, Reverb, or Depop before?*"
    will match the answer key "Have you worked at"
    """
    answers = self.parent_section.ANSWERS.get((type(self)))
    return answers.get(self.name) or key_is_prefix(answers, self.name)

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