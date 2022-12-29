"""
This is a boilerplate pipeline 'data_engineering'
generated using Kedro 0.18.3
"""

from kedro.pipeline import Pipeline, node, pipeline
from projetfinal.pipelines.data_engineering.nodes import nombreTotalImage, create_dataframe, update_culumn_dataframe


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
                func=update_culumn_dataframe,
                inputs=["created_dataset"],
                outputs=["dataset2"],
                name="update_culumn_dataframe"
            ),
    ])
