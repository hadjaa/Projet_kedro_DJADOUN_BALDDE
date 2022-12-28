"""
This is a boilerplate pipeline 'data_engineering'
generated using Kedro 0.18.3
"""

from kedro.pipeline import Pipeline, node, pipeline
from projetfinal.pipelines.data_engineering.nodes import nombreTotalImage, create_dataframe, split_train_test_data, support_vector_machine


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
         node(
                func=nombreTotalImage,
                inputs=["params:base_path"],
                outputs="breast_total_image",
                name="nombreTotalImage"
            ),
             node(
                func=create_dataframe,
                inputs=["params:base_path"],
                outputs="created_dataset",
                name="create_dataframe"
            ),
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
