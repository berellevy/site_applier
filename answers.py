import pandas as pd


def load_answers() -> pd.DataFrame:
  return pd.concat([
    pd.DataFrame(columns=["page", "section", "sub_section", "field_type", "field_name", "answer"], dtype=object),
    pd.read_json("answers.json"),

  ])
_df = load_answers()


def get_sub_sections(*, page, section):
  return list(
    _df.loc[
      (_df["page"] == "My Experience") &
      (_df["section"] == "Work Experience"),
      "sub_section"
    ]
    .unique()
  )
  


def get(
  page: str = None,
  field_type: str = None,
  field_name: str = None,
  section: str = None,
  sub_section: str = None,
):

  base_filters = (
    (_df["page"].eq(page) if page else True) &
    (_df["field_type"].eq(field_type) if field_type else True) &
    (_df["section"].eq(section) if section else True) &
    (_df["sub_section"].eq(sub_section) if sub_section else True) 
  )

  answer = _df.loc[
    base_filters &
    (_df["field_name"].eq(field_name) if field_name else True)
    ,
    "answer"
  ]
  if answer.empty:
    answer = _df.loc[
      base_filters &
      (_df["field_name"].apply(lambda x: field_name.startswith(x)) if field_name else True)
      ,
      "answer"
    ]
  return next(iter(answer.values), None)