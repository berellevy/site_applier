"""xpath util functions"""
from typing import Literal
from .main import WebElement, D, XP

    

def attr_ends_with(attr: str, value: str) -> str:
  """because xpath 1. attr can also be `'text()'`"""
  # TODO: EXPLAIN
  attr = f"@{attr}" if attr != "text()" else attr
  return f"substring({attr}, string-length({attr}) - string-length('{value}') + 1) = '{value}'"


def attr_starts_with(attr: str, value: str) -> str:
  attr = f"@{attr}" if attr != "text()" else attr
  return f"starts-with({attr}, '{value}')"

def attr_contains(attr: str, value: str) -> str:
  attr = f"@{attr}" if attr != "text()" else attr
  return f"contains({attr}, '{value}')"

def d_id(value, match_type: Literal["exact", "startswith", "endswith", "contains"] = "exact") -> str:
  """
  Abbreviation for attribute data-automation-id='value'.
  
  Examples: 
  >>> d_di("hello")
  "@data-automation-id='hello'"
  >>> d_id("hello", match_type="startswith")
  "starts-with(@data-automation-id, 'hello')"
  >>> d_id("hello", match_type="endswith")
  "substring(@data-automation-id, string-length(@data-automation-id) - string-length('hello') + 1) = 'hello'"
  >>> d_id("hello", match_type="contains")
  "contains(@data-automation-id, 'hello')"
  """
  attr = "data-automation-id"
  return {
    "exact": f"@{attr}='{value}'",
    "startswith": attr_starts_with(attr, value),
    "endswith": attr_ends_with(attr, value),
    "contains": attr_contains(attr, value)
  }[match_type]