from browser import D, XP, find_element


class BaseFormField:
  XPATH: str
  NAME_XPATH: str

  @classmethod
  def find_all(cls, browser: D, parent_section):
    return [cls(f, parent_section) for f in browser.find_elements(XP, cls.XPATH)]

  def __init__(self, element: D, parent_section) -> None:
    self.element = element
    self.parent_section = parent_section

  @property
  def name(self) -> str:
    return find_element(self.element, XP, self.NAME_XPATH).text  

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