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
