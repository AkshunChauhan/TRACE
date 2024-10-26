import re
import pandas as pd


# def jaccard_similarity(set1, set2):
#     """Calculate Jaccard similarity between two sets."""
#     intersection = len(set1.intersection(set2))
#     union = len(set1.union(set2))
#     if union == 0:
#         return 0.0
#     return intersection / union


def extract_clos(sheet_data, start_row=12):
    """
    Extract Course Learning Outcomes (CLOs) from Excel sheet data starting from a specific row.

    Args:
        sheet_data (pd.DataFrame): The DataFrame containing the sheet's data.
        start_row (int): The row index from which to start extracting CLOs.

    Returns:
        list: A list of CLO descriptions extracted from the sheet.
    """
    clo_list = []

    # Loop through rows starting from start_row
    for i in range(start_row, len(sheet_data)):
        row = sheet_data.iloc[i]

        if not row.isnull().all():
            # Filter out any columns that contain only CLO identifiers like C1, CLO 1, etc.
            non_nan_values = row.dropna()

            # Check if any CLO identifier exists in the row
            if any(re.match(r"^CLO\s*\d+$", str(desc)) for desc in non_nan_values):
                # If a CLO identifier is found, extract all non-identifier descriptions
                filtered_descriptions = [
                    desc
                    for desc in non_nan_values
                    if desc
                    and not re.match(
                        r"^CLO\s*\d+$", str(desc)
                    )  # Exclude CLO identifiers
                    and not re.match(
                        r"^[C]\d+$", str(desc)
                    )  # Exclude simple identifiers like C1, C2
                ]
                clo_list.extend(filtered_descriptions)
        else:
            # Stop if an empty row is encountered
            break

    return clo_list
