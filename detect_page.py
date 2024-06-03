# from typing import Literal
# from browser import CSS, D, find_element, el_text_content

# def data_id_find(el, data_id, starts_with=False):
#   if starts_with:
#     modifier = "^"
#   else:
#     modifier = ""
#   return (CSS, f"{el}[data-automation-id{modifier}='{data_id}']")

# PAGE_TYPE = Literal[
#  "JOB_DESCRIPTION",
#   "SIGN_IN_WRONG_PASSWORD",
#   "SIGN_IN",
#   "CREATE_ACCOUNT",
#   "CREATE_ACCOUNT_EXISTS_ERROR",
#   "FORGOT_PASSWORD",
#   "RESET_PASSWORD",
#   "ALREADY_APPLIED",
#   "MY_INFORMATION",
#   "MY_EXPERIENCE",
#   "APPLICATION_QUESTIONS",
#   "VOLUNTARY_DISCLOSURES",
#   "REVIEW",
#   "SUCCESS",

#   "UNKNOWN_PAGE",
# ]

# from pages import PAGES, BasePage

# def detect_page(browser: D) -> BasePage:
#   for page in PAGES:
#     if page.is_current(browser):
#       return page
  
#   if (
#     find_element(browser, *el_text_content("h2", "Sign In")) and
#     find_element(browser, *data_id_find("div", "errorMessage"))
#   ):
#     return "SIGN_IN_WRONG_PASSWORD"
#   elif find_element(browser, *el_text_content("h2", "Sign In")):
#     return "SIGN_IN"
  
#   elif (
#     find_element(browser, *el_text_content("h2", "Create Account")) and
#     find_element(browser, *data_id_find("div", "errorMessage"))
#   ):
#     return "CREATE_ACCOUNT_EXISTS_ERROR"
#   elif find_element(browser, *el_text_content("h2", "Create Account")):
#     return "CREATE_ACCOUNT"
  
#   elif find_element(browser, *el_text_content("h2", "Forgot Password")):
#     return "FORGOT_PASSWORD"
  
#   elif find_element(browser, *el_text_content("h2", "Reset Password")):
#     return "RESET_PASSWORD"
  
#   if find_element(browser, *data_id_find("div", "alreadyApplied")):
#     return "ALREADY_APPLIED"

#   elif find_element(browser, *el_text_content("h2", "My Information")):
#     return "MY_INFORMATION"
  
#   elif find_element(browser, *el_text_content("h2", "My Experience")):
#     return "MY_EXPERIENCE"
  
#   elif find_element(browser, *el_text_content("h2", "Application Questions")):
#     return "APPLICATION_QUESTIONS"
  
#   elif find_element(browser, *el_text_content("h2", "Voluntary Disclosures")):
#     return "VOLUNTARY_DISCLOSURES"
  
#   elif find_element(browser, *el_text_content("h2", "Review")):
#     return "REVIEW"
  
#   if find_element(browser, *data_id_find("div", "congratulationsPopup")):
#     return "SUCCESS"
  
#   else:
#     return "UNKNOWN_PAGE"  
  