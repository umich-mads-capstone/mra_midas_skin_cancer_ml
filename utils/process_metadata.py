from pathlib import Path

import pandas as pd


def get_file_path():
    """Get the file path to the MIDAS dataset Excel file."""
    project_root = Path(__file__).parent.parent.parent
    file_path = (
        project_root
        / "mra_midas_skin_cancer_ml"
        / "data"
        / "input"
        / "release_midas.xlsx"
    )
    return file_path


def import_metadata(file_path=None):
    """
    Helper function to import MIDA dataset for both metadata and
    image modeling tasks.
    """
    if file_path is None:
        file_path = get_file_path()

    excel_data = pd.ExcelFile(file_path)

    # Read the first sheet by default
    sheet_name = excel_data.sheet_names[0]
    df = excel_data.parse(sheet_name)

    return df
