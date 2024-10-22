import pandas as pd
import re

def extract_clos(data, start_row=12, start_col=1, end_col=None):
    """Extract Course Learning Outcomes (CLOs) from Excel data."""
    clo_list = []
    for i in range(start_row, len(data)):
        row = data.iloc[i]
        if not row.isnull().all():
            non_nan_values = row.dropna()
            if len(non_nan_values) > 1:
                clo_descriptions = non_nan_values[start_col:end_col].tolist()
                filtered_descriptions = [desc for desc in clo_descriptions if not re.match(r'^[C]\d+$', str(desc))]
                clo_list.extend(filtered_descriptions)
        else:
            break
    return clo_list

def extract_clos_from_file(file_path):
    """Read and extract CLOs from an Excel file."""
    data = pd.read_excel(file_path)
    return extract_clos(data)
