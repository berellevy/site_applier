from browser import D


class BaseFormField:
  def __init__(self, element: D, parent_section = None) -> None:
    self.element = element
    self.parent_section = parent_section

  @property
  def parent_name(self) -> str:
    return f"{self.parent_section.name}." if self.parent_section else ""
  
  def __repr__(self) -> str:
    classname = type(self).__name__
    name = getattr(self, "name", "")
    required = 'required, ' if getattr(self, "is_required", False) else ''
    correct_answer = f", answer: {answer}" if (answer:=getattr(self, "correct_answer", False)) else ""
    return f"<{classname}: {required}{name}{correct_answer}>"