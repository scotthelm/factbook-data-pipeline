from typing import List
import pandas as pd
from kedro.pipeline import Pipeline, node
from factbook_data_pipeline.utils import load_geo_codes
from .nodes import(
    convert_api_to_json
)

def create_pipeline(**kwargs):
    geo_codes = load_geo_codes()
    nodes = create_nodes(geo_codes)
    return Pipeline(nodes)

def create_nodes(geo_codes: pd.DataFrame) -> List:
    nodes = []
    for _index, row in geo_codes.iterrows():
        nodes.append(
            node(
                func=convert_api_to_json,
                inputs=[f'{row["code"]}_api_dataset', f'{row["code"]}_name_dataset'],
                outputs=f'{row["code"]}_json_dataset',
                name=f'convert_{row["code"]}_api_to_json'
            )
        )
    return nodes
