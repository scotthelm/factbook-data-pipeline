import pandas as pd
import re
from kedro.extras.datasets.yaml import YAMLDataSet


def clean_columns(
    to_clean: pd.DataFrame,
    cleaning_config: dict
) -> pd.DataFrame:
    for key in cleaning_config['field_cleaning']:
        config = cleaning_config['field_cleaning'][key]
        to_clean[config['rename_to']] = to_clean.apply(
            lambda x: clean(x[key], config['replacement_regex']),
            axis=1
        )
    return to_clean

def clean(value: str, regexes: list) -> str:
    if not isinstance(value, str):
        return None
    else:
        for r in regexes:
            value = re.sub(r, '', value)
        return value