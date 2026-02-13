from pathlib import Path

import pandas as pd


def import_metadata(input_path="data/input/release_midas.xlsx"):
    """Helper function to import metadata."""
    project_root = Path(__file__).parent.parent.parent
    file_path = (
        project_root
        / "mra_midas_skin_cancer_ml"
        / "data"
        / "input"
        / "release_midas.xlsx"
    )
    excel_data = pd.ExcelFile(file_path)

    # Read the first sheet by default
    sheet_name = excel_data.sheet_names[0]
    df = excel_data.parse(sheet_name)

    return df
    return df
