from typing import List
import pandas as pd
import os.path
from kedro.pipeline import Pipeline, node
from .nodes import(
    convert_api_to_json
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
                func=convert_api_to_json,
                inputs=f'{row["code"]}_api_dataset',
                outputs=f'{row["code"]}_json_dataset',
                name=f'convert_{row["code"]}_api_to_json'
            )
        )
    return nodes