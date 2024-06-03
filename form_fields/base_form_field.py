from browser import D


class BaseFormField:
  def __init__(self, element: D) -> None:
    self.element = element
  
  def __repr__(self) -> str:
    classname = type(self).__name__
    name = getattr(self, "name", "")
    required = ', required' if getattr(self, "is_required", False) else ''
    correct_answer = f", answer: {answer}" if (answer:=getattr(self, "correct_answer", False)) else ""
    return f"<{classname}: {name}{required}{correct_answer}>"