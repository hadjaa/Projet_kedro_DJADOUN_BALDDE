"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 0.18.3
"""
from kedro.pipeline import Pipeline, node, pipeline
from projetfinal.pipelines.data_science.nodes import split_train_test_data, support_vector_machine


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([

        node(
                func=split_train_test_data,
                inputs=["created_dataset", "params:test_size"],
                outputs=["x_train", "x_test", "y_train", "y_test"],
                name="split_train_test_data"
            ),
            node(
                func=support_vector_machine,
                inputs=["x_train", "x_test", "y_train"],
                outputs=["pred"],
                name="support_vector_machine"
            ),
            
    ])
