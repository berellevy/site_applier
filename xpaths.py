from browser import xp_attr_ends_with, xp_attr_starts_with

####################### FORM INPUTS ######################
FORM_MULTISECTION = (
  "//div"
  f"[{xp_attr_ends_with('data-automation-id', 'Section')}]"
  f"[.//button[{xp_attr_starts_with('text()', 'Add')}]]"
)

MULTISECTION_EXCLUDER = f"[not(ancestor::{FORM_MULTISECTION.removeprefix('//')})]"

FORM_TEXT_INPUT = (
  ".//div"
  f"[{xp_attr_starts_with('data-automation-id', 'formField-')}]"
  f"[.//input[@type='text'] or .//input[@type='password']]"
  f"[not(.//*[@aria-haspopup])]"
  f"{MULTISECTION_EXCLUDER}"
)

FORM_DROPDOWN = (
  ".//div"
  f"[{xp_attr_starts_with('data-automation-id', 'formField-')}]"
  "[.//button[@aria-haspopup='listbox']]"
  f"{MULTISECTION_EXCLUDER}"

)

FORM_MULTISELECT_SEARCH = (
  ".//div"
  f"[{xp_attr_starts_with('data-automation-id', 'formField-')}]"
  f"[.//div[@data-automation-id='multiselectInputContainer']]"
  f"{MULTISECTION_EXCLUDER}"
)

FORM_RADIO = (
  ".//div"
  f"[{xp_attr_starts_with('data-automation-id', 'formField-')}]"
  "[.//input[@type='radio']]"
  f"{MULTISECTION_EXCLUDER}"
)

####################### PAGES #############################
JOB_DESCRIPTION_PAGE = """
  //body[
    .//div[@data-automation-id="jobPostingPage"] 
    and not(.//h2[contains(text(),"Start Your Application")])
  ]
"""

START_APPLICATION_PAGE = """
  //body[
    .//div[@data-automation-id="jobPostingPage"] 
    and .//h2[contains(text(),"Start Your Application")]
  ]
"""

SIGN_IN_PAGE = """
  //div[
    @id='mainContent' and 
    .//h2[text()='Sign In'] 
    and not(.//div[@data-automation-id='errorMessage'])
  ]
"""

MY_INFORMATION_PAGE = f"//h2[{xp_attr_starts_with('text()', 'My Information')}]"

MY_EXPERIENCE_PAGE = f"//h2[{xp_attr_starts_with('text()', 'My Experience')}]"