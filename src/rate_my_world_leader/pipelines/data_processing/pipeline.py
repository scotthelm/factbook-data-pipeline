from typing import List
import pandas as pd
import os.path
from kedro.pipeline import Pipeline, node
from .nodes import(
    convert_json_to_dataframe
)

def create_pipeline(**kwargs):
    geo_codes = load_geo_codes()
    nodes = create_nodes(geo_codes)
    return Pipeline(nodes)

def load_geo_codes():
    if os.path.isfile('conf/local/factbook_codes_normalized.csv'):
        df = pd.read_csv('conf/local/factbook_codes_normalized.csv')
    else:
        df = pd.DataFrame()
    return df

def create_nodes(geo_codes: pd.DataFrame) -> List:
    nodes = []
    for _index, row in geo_codes.iterrows():
        nodes.append(
            node(
                func=convert_json_to_dataframe,
                inputs=f'{row["code"]}_json_dataset',
                outputs=f'{row["code"]}_intermediate_csv_dataset',
                name=f'convert_{row["code"]}_json_to_intermediate_csv'
            )
        )
    return nodes