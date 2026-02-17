"""
Utility functions for processing the MIDAS metadata Excel file.
"""

from pathlib import Path

import pandas as pd


def get_data_dir():
    """Return the path to the project's data directory."""
    project_root = Path(__file__).parent.parent.parent
    data_dir = project_root / "mra_midas_skin_cancer_ml" / "data"

    return data_dir


def import_metadata(file_path=None):
    """
    Helper function to import MIDA dataset for both metadata and
    image modeling tasks.
    """
    if file_path is None:
        file_path = get_data_dir() / "input" / "release_midas.xlsx"

    excel_data = pd.ExcelFile(file_path)

    # Read the first sheet by default
    sheet_name = excel_data.sheet_names[0]
    df = excel_data.parse(sheet_name)

    return df


def label_benign(row):
    """
    Label the row as 'benign' or 'malignant' based on the content
    of the row.
    """
    if row == "missing":
        return "missing"

    parts = row.split("-")
    parts = [p.lower().strip() for p in parts]

    if "benign" in parts:
        return "benign"

    # Assume benign - not stated in midas_path
    row_lower = row.lower()
    if any(keyword in row_lower for keyword in ["non-neoplastic"]):
        return "benign"

    # Assume malignant - not stated in midas_path
    if any(
        keyword in row_lower
        for keyword in ["melanocytic tumor", "other-melanocytic lesion"]
    ):
        return "malignant"

    return "malignant"


def process_target(df):
    """Impute target feature and create binary target feature."""

    # For controls, use the clinical impression 1 to determine benign vs malignant
    df.loc[df["midas_iscontrol"] == "yes", "midas_path"] = df[
        "clinical_impression_1"
    ]

    df["midas_path"] = df["midas_path"].fillna("missing")

    df["midas_path_binary"] = df["midas_path"].apply(label_benign)

    return df


def export_metadata(df, file_path=None):
    """Export the processed metadata to a new Excel file."""
    if file_path is None:
        file_path = get_data_dir() / "output" / "processed_metadata.xlsx"

    df.to_excel(file_path, index=False)


def create_lesion_key(df):
    """
    Create a unique key for each lesion based on patient ID,
    location, and size.
    """

    key_df = df.copy()

    key_df["lesion_key"] = (
        key_df["midas_record_id"].astype(str)
        + "_"
        + key_df["midas_location"].astype(str)
        + "_"
        + key_df["length_(mm)"].astype(str)
        + "x"
        + key_df["width_(mm)"].astype(str)
    )
    return key_df


def sort_metadata(df):
    """Sort metadata by patient ID, lesion location, and control status."""

    sorted_df = df.sort_values(
        by=[
            "midas_record_id",  # patient ID
            "midas_location",  # lesion location
            "midas_iscontrol",  # control vs non-control (yes -> no)
        ],
        ascending=[True, True, False],
    )

    return sorted_df


def dedupe_metadata(df):
    """
    Helper function to de-duplicate metadata.
    Returns a DataFrame with one row per lesion.
    """

    cols = [
        "midas_path_binary",
        "midas_record_id",
        "midas_location",
        "midas_age",
        "midas_fitzpatrick",
        "midas_ethnicity",
        "midas_race",
        "length_(mm)",
        "width_(mm)",
    ]

    metadata_df = df.copy()

    # Sort "midas_iscontrol" by descending (yes -> no)
    # to keep the last record which is the non-control
    # if there are duplicates due to data quality issues.
    metadata_df = sort_metadata(metadata_df)

    # Remove duplicates (three images per lesion)
    metadata_df = metadata_df[cols].drop_duplicates()

    # Create a unique key per patient and lesion
    metadata_df = create_lesion_key(metadata_df)

    # There are 26 records that are duplicates due to data quality issues.
    # Keep the last one or the non-controls if due to "midas_iscontrol" issues.
    metadata_df = metadata_df.drop_duplicates(subset="lesion_key", keep="last")

    # Check for uniqueness
    print(metadata_df["lesion_key"].is_unique)

    # Add integer index
    metadata_df = metadata_df.reset_index(drop=True)
    metadata_df.index.name = "row_id"

    # Return meta_df
    return metadata_df
