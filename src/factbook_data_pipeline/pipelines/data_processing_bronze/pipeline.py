from .nodes import (
    combine,
    create_column_analysis,
    filter_bronze_dataset_columns,
    intermediate_dataset_names,
)
from kedro.pipeline import Pipeline, node

def create_pipeline(**kwargs):
    return Pipeline([
        node(
            func=combine,
            inputs=intermediate_dataset_names(),
            outputs='unfiltered_bronze_dataset',
            name='combine_intermediate_datasets_to_bronze'
        ),
        node(
            func=create_column_analysis,
            inputs='unfiltered_bronze_dataset',
            outputs='bronze_column_analysis_dataset',
            name='create_column_analysis'
        ),
        node(
            func=filter_bronze_dataset_columns,
            inputs=['unfiltered_bronze_dataset', 'bronze_column_analysis_dataset'],
            outputs='filtered_bronze_dataset',
            name='filter_bronze_dataset_columns'
        ),
    ])
