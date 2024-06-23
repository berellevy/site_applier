"""xpaths used by form_fields and pages to find their elements."""

from utils import xp, d_id
####################### FORM INPUTS ######################
FORM_MULTISECTION = (
  "//div"
  f"[{d_id('Section', "endswith")}]"
  f"[.//button[{xp.attr_starts_with('text()', 'Add')}]]"
)

MULTISECTION_EXCLUDER = f"[not(ancestor::{FORM_MULTISECTION.removeprefix('//')})]"

FORM_TEXT_INPUT = (
  ".//div"
  f"[{d_id('formField-', "startswith")}]"
  f"[.//input[@type='text'] or .//input[@type='password']]"
  f"[not(.//*[@aria-haspopup])]"
  f"{MULTISECTION_EXCLUDER}"
)

FORM_TEXT_AREA = (
  ".//div"
  f"[{d_id('formField-', "startswith")}]"
  "[.//textarea]"
  f"{MULTISECTION_EXCLUDER}"
)

FORM_DROPDOWN = (
  ".//div"
  f"[{d_id('formField-', "startswith")}]"
  "[.//button[@aria-haspopup='listbox']]"
  f"{MULTISECTION_EXCLUDER}"

)

FORM_MULTISELECT_SEARCH = (
  ".//div"
  f"[{d_id('formField-', "startswith")}]"
  f"[.//div[{d_id('multiselectInputContainer')}]]"
  f"{MULTISECTION_EXCLUDER}"
)

FORM_RADIO = (
  ".//div"
  f"[{d_id('formField-', "startswith")}]"
  "[.//input[@type='radio']]"
  f"{MULTISECTION_EXCLUDER}"
)

FORM_SINGLE_CHECKBOX = (
  ".//div"
  f"[{d_id('formField-', "startswith")}]"
  f"[count(.//input[@type='checkbox']) = 1]"
  f"{MULTISECTION_EXCLUDER}"
)

FORM_MONTH_YEAR = (
  ".//div"
  f"[{d_id('formField-', "startswith")}]"
  "[.//input[@aria-label='Month']]"
  "[.//input[@aria-label='Year']]"
  f"{MULTISECTION_EXCLUDER}"
)

####################### PAGES #############################
JOB_DESCRIPTION_PAGE = (
    "//body"
    f"[.//div[{d_id('jobPostingPage')}]" 
    "[not(.//h2[contains(text(),'Start Your Application')])]"
)

START_APPLICATION_PAGE = (
  "//body"
  "[//h2[contains(text(),'Start Your Application')]]"
)

SIGN_IN_PAGE = (
  "//div"
  "[@id='mainContent']" 
  "[.//h2[text()='Sign In']]" 
  f"[not(.//div[{d_id('errorMessage')}])]"
)

REVIEW_PAGE = f"//h2[{xp.attr_starts_with('text()', 'Review')}]"

MY_INFORMATION_PAGE = (
    "//body"
    f"[//h2[{xp.attr_starts_with('text()', 'My Information')}]]"
    f"[not({REVIEW_PAGE})]"
)

MY_EXPERIENCE_PAGE = (
    "//body"
    f"[//h2[{xp.attr_starts_with('text()', 'My Experience')}]]"
    f"[not({REVIEW_PAGE})]"
)

APPLICATION_QUESTIONS_PAGE = (
    "//body"
    f"[//h2[{xp.attr_starts_with('text()', 'Application Questions')}]]"
    f"[not({REVIEW_PAGE})]"
)

VOLUNTARY_DISCLOSURES_PAGE = (
    "//body"
    f"[//h2[{xp.attr_starts_with('text()', 'Voluntary Disclosures')}]]"
    f"[not({REVIEW_PAGE})]"
)

ALREADY_APPLIED_PAGE = (
    "//body"
    f"[//h2[{xp.attr_contains('text()', 'already applied for this job')}]]"
)