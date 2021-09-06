from .nodes import combine_intermediate_datasets_to_bronze
from kedro.pipeline import Pipeline, node

def create_pipeline(**kwargs):
    return Pipeline([
        node(
            func=combine_intermediate_datasets_to_bronze,
            inputs=None,
            outputs='combined_bronze_dataset',
            name='combine_intermediate_datasets_to_bronze'
        )
    ])