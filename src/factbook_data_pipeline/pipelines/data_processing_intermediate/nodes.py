import pandas as pd
import re

from pandas.core.frame import DataFrame
from factbook_data_pipeline.utils import load_geo_codes
from kedro.extras.datasets.pandas import CSVDataSet


def convert_json_to_dataframe(json_data: dict) -> pd.DataFrame:
    df = pd.json_normalize(json_data)
    original_columns = list(df.columns)
    renamed_columns = list(
        map(
            lambda x: re.sub(
                r'\W',
                '',
                x.lower().replace('.text', '').replace(' ', '_').replace('.', '_').replace('-', '_').replace('___', '_'))
                , original_columns
        )
    )
    zipped_columns = zip(original_columns, renamed_columns)
    dictionary_for_renaming = dict((x, y) for (x, y) in zipped_columns)
    df.rename(columns=dictionary_for_renaming, inplace=True)
    return df
