from .nodes import combine, intermediate_dataset_names
from kedro.pipeline import Pipeline, node

def create_pipeline(**kwargs):
    return Pipeline([
        node(
            func=combine,
            inputs=intermediate_dataset_names(),
            outputs='combined_bronze_dataset',
            name='combine_intermediate_datasets_to_bronze'
        )
    ])
