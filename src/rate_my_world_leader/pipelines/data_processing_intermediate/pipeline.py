from typing import List
import pandas as pd
from kedro.pipeline import Pipeline, node
from rate_my_world_leader.utils import load_geo_codes
from .nodes import(
    convert_json_to_dataframe,
)

def create_pipeline(**kwargs):
    geo_codes = load_geo_codes()
    nodes = create_nodes(geo_codes)
    return Pipeline(nodes)

def create_nodes(geo_codes: pd.DataFrame) -> List:
    nodes = []
    inputs = []
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
