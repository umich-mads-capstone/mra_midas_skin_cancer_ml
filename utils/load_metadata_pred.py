"""
Utility functions to help load metadata prediction results back into the
master lesion-level dataframe for late fusion analysis.
"""

import pandas as pd

from mra_midas_skin_cancer_ml.utils.process_metadata import get_data_dir

DATA_OUTPUT_DIR = get_data_dir() / "output"
METADATA_MODEL_DIR = DATA_OUTPUT_DIR / "metadata_model_output"



def load_pred_file():
    """Load exactly one prediction file."""

    model_dir = METADATA_MODEL_DIR
    files = list(model_dir.glob(f"*_predictions.xlsx"))

    if not files:
        raise FileNotFoundError(
            f"No prediction file found.."
        )

    if len(files) > 1:
        file_names = [f.name for f in files]
        raise ValueError(
            f"Expected exactly one prediction file, "
            f"but found {len(files)}: {file_names}"
        )

    return pd.read_excel(files[0])
