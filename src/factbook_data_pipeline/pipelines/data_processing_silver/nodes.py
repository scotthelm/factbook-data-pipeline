import json
import pandas as pd
from factbook_data_pipeline.cleaning import clean


def clean_columns(
    to_clean: pd.DataFrame,
    cleaning_config: dict
) -> pd.DataFrame:
    for key in cleaning_config['field_cleaning']:
        config = cleaning_config['field_cleaning'][key]

        clean(to_clean, key, config)
    return to_clean

def to_silver_table_dataset(data: pd.DataFrame, config: dict) -> pd.DataFrame:
    dtypes = config['silver_table_dataset']['save_args']['dtype']
    for key, value in dtypes.items():
        if value.find('Json'):
            series = data.apply(
                lambda x: json.loads(x[key]),
                axis=1
            )
            data[key] = series
    return data
