from .nodes import combine_intermediate_datasets_to_bronze, intermediate_dataset_names
from kedro.pipeline import Pipeline, node

def create_pipeline(**kwargs):
    nodes = input_nodes()
    return Pipeline(nodes)

def input_nodes():
    nodes = []
    for name in intermediate_dataset_names():
        nodes.append(
            node(
                func=lambda x: x,
                inputs=name,
                outputs=None
            )
        )
    nodes.append(
        node(
            func=combine_intermediate_datasets_to_bronze,
            inputs=None,
            outputs='combined_bronze_dataset',
            name='combine_intermediate_datasets_to_bronze'
        )
    )
    return nodes