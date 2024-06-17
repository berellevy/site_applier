import pandas as pd

_df = pd.read_json("answers.json")


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

    exact_match = _df.loc[
        base_filters &
        (_df["field_name"].eq(field_name) if field_name else True)
        ,
        "answer"
    ]
    if exact_match.empty:
        print(field_name)
        startswith = _df.loc[
            base_filters &
            (_df["field_name"].apply(lambda x: field_name.startswith(x)) if field_name else True)
            ,
            "answer"
        ]
        return list(startswith)
    return list(exact_match)