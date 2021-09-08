from pandas.core.frame import DataFrame
from kedro.framework.session import get_current_session
from kedro.extras.datasets.pandas import CSVDataSet
from rate_my_world_leader.utils import load_geo_codes
import pandas as pd

def combine(*argv) -> pd.DataFrame:
    combined_dataset = pd.DataFrame()
    for df in argv:
        combined_dataset = combined_dataset.append(df, ignore_index=True)

    return combined_dataset

def intermediate_dataset_names():
    ds_names = []
    for _index, row in load_geo_codes().iterrows():
        ds_names.append(
            f'{row["code"]}_intermediate_csv_dataset'
        )
    return ds_names

def create_column_analysis(unfiltered_bronze_dataset: pd.DataFrame) -> pd.DataFrame:
    column_df = pd.DataFrame()
    column_df['count'] = unfiltered_bronze_dataset.count(0)
    column_df['percentage_of_max'] = column_df.apply(
        lambda x : x / column_df['count'].max()
    )
    column_df['should_remove'] = column_df.apply(lambda x: x['percentage_of_max'] < 0.5, axis=1)
    column_df['index_length'] = column_df.index.str.len()
    column_df['index_name'] = list(column_df.index)
    return column_df

def filter_bronze_dataset_columns(
    unfiltered_bronze_dataset: pd.DataFrame,
    bronze_column_analysis_dataset: pd.DataFrame
) -> pd.DataFrame:
    unfiltered = unfiltered_bronze_dataset
    analysis = bronze_column_analysis_dataset
    columns_to_filter = list(analysis.loc[analysis['should_remove'] == True]['index_name'])
    unfiltered.drop(columns_to_filter, inplace=True, axis=1)
    return unfiltered