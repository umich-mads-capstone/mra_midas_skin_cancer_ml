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
    """Load the most recent prediction file for the specified split."""

    split_dir = IMAGE_MODEL_DIR / split
    files = list(split_dir.glob("*_predictions.xlsx"))
    return max(files, key=lambda f: f.stat().st_mtime) if files else None


def merge_image_pred():
    """Merge the image prediction results back into the master lesion-level dataframe."""

    splits = ["1ft", "6in", "dscope"]

    master_df = pd.read_excel(
        DATA_OUTPUT_DIR / "split_keys" / "master_lesion_split_lookup.xlsx"
    )
    master_df = master_df[master_df["split"] == "test"].copy()
    key_dfs = load_image_split_keys(splits)

    for split in splits:
        pred_file = load_pred_file(split)
        if pred_file is None:
            continue

        model_prefix = pred_file.stem.split("_")[0].lower()
        pred_df = pd.read_excel(pred_file).rename(
            columns={
                "probability_score": f"{model_prefix}_{split}_probability_score",
                "prediction_label": f"{model_prefix}_{split}_prediction_label",
            }
        )

        key_df = key_dfs[split]
        key_df_test = key_df[key_df["split"] == "test"]

        split_pred_df = key_df_test.merge(
            pred_df,
            left_on=["matched_file", "midas_path_binary"],
            right_on=["file_name", "actual_label"],
            how="left",
        ).drop(
            columns=[
                "midas_record_id",
                "midas_file_name",
                "matched_file",
                "midas_path_binary",
                "split",
                "file_name",
                "actual_label",
            ]
        )

        master_df = master_df.merge(split_pred_df, on="lesion_key", how="left")

    return master_df
