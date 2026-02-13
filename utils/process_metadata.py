import pandas as pd

def import_metadata(input_path='data/input/release_midas.xlsx'):
    """Helper function to import metadata."""
    file_path = input_path
    excel_data = pd.ExcelFile(file_path)

    # Read the first sheet by default
    sheet_name = excel_data.sheet_names[0]
    df = excel_data.parse(sheet_name)
    
    return df