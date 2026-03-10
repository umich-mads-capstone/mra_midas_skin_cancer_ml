"""
Utility functions to help merge image prediction results back into the
master lesion-level dataframe for late fusion analysis.
"""

import pandas as pd

from mra_midas_skin_cancer_ml.utils.process_metadata import get_data_dir

DATA_OUTPUT_DIR = get_data_dir() / "output"
IMAGE_MODEL_DIR = DATA_OUTPUT_DIR / "image_model_output"


def load_image_split_keys(splits):
    """Load the split key dataframes for the specified splits."""

    split_key_dfs = {
        split: pd.read_excel(
            DATA_OUTPUT_DIR / "split_keys" / f"{split}_split_image_data.xlsx"
        )
        for split in splits
    }
    return split_key_dfs


def load_pred_file(split):
    """Load the best prediction file for the specified split."""

    pred_files = {
        "1ft": IMAGE_MODEL_DIR
        / split
        / "ResNet_20260309_222933_predictions.xlsx",
        "6in": IMAGE_MODEL_DIR
        / split
        / "ResNet_20260309_223847_predictions.xlsx",
        "dscope": IMAGE_MODEL_DIR
        / split
        / "ResNet_20260309_222158_predictions.xlsx",
    }

    return pred_files.get(split)


def merge_image_pred():
    """Merge the image prediction results back into the master lesion-level dataframe."""

    splits = ["1ft", "6in", "dscope"]

    key_dfs = load_image_split_keys(splits)
    split_pred_dfs = {}

    for split in splits:
        pred_file = load_pred_file(split)
        if pred_file is None:
            continue

        model_prefix = pred_file.stem.split("_")[0].lower()
        pred_df = pd.read_excel(pred_file).rename(
            columns={
                "malignant_probability": f"{model_prefix}_{split}_malignant_probability",
                "prediction_label": f"{model_prefix}_{split}_prediction_label",
            }
        )

        key_df = key_dfs[split]
        print(f"Length of {split} key_df: {len(key_df)}")
        print(f"Length of {split} pred_df: {len(pred_df)}")

        split_pred_df = key_df.merge(
            pred_df,
            left_on=["matched_file"],
            right_on=["file_name"],
            how="left",
        )
        print(f"Length of {split} merged pred: {len(split_pred_df)}")
        split_pred_dfs[split] = split_pred_df

    return split_pred_dfs
