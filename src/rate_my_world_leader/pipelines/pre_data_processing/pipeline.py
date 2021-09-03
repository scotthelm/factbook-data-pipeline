from kedro.pipeline import Pipeline, node
from .nodes import(
    convert_api_to_csv_dataset,
    normalize_factbook_codes
)

def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=convert_api_to_csv_dataset,
                inputs="factbook_codesxref_api",
                outputs="factbook_codesxref",
                name="convert_codesxref_from_api_to_dataset",
            ),
            node(
                func=convert_api_to_csv_dataset,
                inputs="factbook_codes_api",
                outputs="factbook_codes",
                name="convert_codes_from_api_to_dataset",
            ),
            node(
                func=normalize_factbook_codes,
                inputs="factbook_codes",
                outputs="factbook_codes_normalized",
                name="normalize_factbook_codes",
            ),
        ]
    )
