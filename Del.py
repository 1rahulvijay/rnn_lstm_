import pandas as pd
from datetime import datetime, timedelta

# Assuming data is already loaded into a DataFrame
# HU_tbl_LIMITS = pd.read_csv('HU_tbl_LIMITS.csv')

# Convert the CHECKER_DT_STAMP to datetime if it's not already in that format
HU_tbl_LIMITS['CHECKER_DT_STAMP'] = pd.to_datetime(HU_tbl_LIMITS['CHECKER_DT_STAMP'])

# Define the reference date to compare with CHECKER_DT_STAMP
reference_date = datetime.now() - timedelta(days=(2024-1899)*365 + 30)  # Adjust the days count accordingly

# Filter conditions based on the SQL query
filtered_df = HU_tbl_LIMITS[
    (HU_tbl_LIMITS['RECORD_STAT'] == "0") &
    (HU_tbl_LIMITS['CHECKER_DT_STAMP'] < reference_date) &
    ((HU_tbl_LIMITS['MANUAL_LINE'] == "N") | (HU_tbl_LIMITS['MANUAL_LINE'].isnull()))
]

# Select the required columns
selected_df = filtered_df[[
    'LIAB_ID',
    'LINE_CD',
    'LINE_SERIAL',
    'MAIN_LINE',
    'AVAILABILITY_FLAG',
    'LIMIT_AMOUNT',
    'RECORD_STAT',
    'CHECKER_DT_STAMP',
    'MAKER_ID',
    'MANUAL_LINE'
]]

# Sort the DataFrame by 'LIAB_ID'
result_df = selected_df.sort_values(by='LIAB_ID')

print(result_df)
