from .nodes import(
    clean_columns,
    to_silver_table_dataset,
)
from kedro.pipeline import Pipeline, node

def create_pipeline(**kwargs):
    return Pipeline([
        node(
            func=clean_columns,
            inputs=['filtered_bronze_dataset', 'field_cleaning_dataset'],
            outputs='silver_csv_dataset',
            name='clean_columns'
        ),
        node(
            func=to_silver_table_dataset,
            inputs=['silver_csv_dataset', 'catalog_config'],
            outputs='silver_table_dataset',
            name='import_silver_table_dataset',
        ),
    ])