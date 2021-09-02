from kedro.pipeline import Pipeline, node
from .nodes import convert_api_to_csv_dataset

def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=convert_api_to_csv_dataset,
                inputs="factbook_codesxref_api",
                outputs="factbook_codesxref",
                name="convert_codesxref_from_api_to_dataset",
            ),
        ]
    )
