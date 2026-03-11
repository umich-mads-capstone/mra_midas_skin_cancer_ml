"""
Utility functions to help merge image prediction results back into the
master lesion-level dataframe for late fusion analysis.
"""

import pandas as pd

from mra_midas_skin_cancer_ml.utils.process_metadata import get_data_dir

DATA_OUTPUT_DIR = get_data_dir() / "output"
IMAGE_MODEL_DIR = DATA_OUTPUT_DIR / "image_model_output"


def load_image_split_keys(dists):
    """Load the split key dataframes for the specified dists."""

    split_key_dfs = {
        dist: pd.read_excel(
            DATA_OUTPUT_DIR / "split_keys" / f"{dist}_split_image_data.xlsx"
        )
        for dist in dists
    }
    return split_key_dfs


def load_pred_file(dist, split):
    """Load exactly one prediction file for a given distance and split."""

    model_dir = IMAGE_MODEL_DIR / dist
    files = list(model_dir.glob(f"*_{split}_predictions.xlsx"))

    if not files:
        raise FileNotFoundError(
            f"No prediction file found for dist='{dist}', split='{split}' in {model_dir}."
        )

    if len(files) > 1:
        file_names = [f.name for f in files]
        raise ValueError(
            f"Expected exactly one prediction file for dist='{dist}', split='{split}', "
            f"but found {len(files)}: {file_names}"
        )

    return files[0]


def merge_image_pred():
    """Return one merged dataframe per distance with split-key metadata."""

    dists = ["1ft", "6in", "dscope"]
    splits = ["train", "val", "test"]
    output = {}
    key_dfs = load_image_split_keys(dists)

    for dist in dists:
        split_merged_dfs = []
        key_df_all = key_dfs[dist]

        for split in splits:
            pred_file = load_pred_file(dist, split)
            pred_df = pd.read_excel(pred_file)
            key_df = key_df_all[key_df_all["split"] == split].copy()

            pred_subset = pred_df[
                ["file_name", "malignant_probability", "prediction_label"]
            ].rename(
                columns={
                    "malignant_probability": f"{dist}_malignant_probability",
                    "prediction_label": f"{dist}_prediction_label",
                }
            )

            merged_df = key_df.merge(
                pred_subset,
                left_on="matched_file",
                right_on="file_name",
                how="left",
            )
            if "file_name" in merged_df.columns:
                merged_df = merged_df.drop(columns=["file_name"])

            split_merged_dfs.append(merged_df)

            print(f"Length of {dist}-{split} key rows: {len(key_df)}")
            print(f"Length of {dist}-{split} pred rows: {len(pred_df)}")
            print(f"Length of {dist}-{split} merged rows: {len(merged_df)}")

        output[dist] = pd.concat(split_merged_dfs, ignore_index=True)
        print(f"Length of {dist} combined rows: {len(output[dist])}")

    return output
