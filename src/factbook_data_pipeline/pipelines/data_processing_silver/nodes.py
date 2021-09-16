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

def to_silver_table_dataset(data: pd.DataFrame) -> pd.DataFrame:
    return data