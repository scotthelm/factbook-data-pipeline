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

