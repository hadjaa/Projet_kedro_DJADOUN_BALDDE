"""Project pipelines."""
from typing import Dict

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline
from projetfinal.pipelines.data_engineering import pipeline as dp

def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    data_processing_pipeline = dp.create_pipeline()
    
    return {
        
                    "__default__": data_processing_pipeline,
                    "dp": data_processing_pipeline

    }