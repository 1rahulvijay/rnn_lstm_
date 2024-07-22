import pandas as pd
import numpy as np
import xlsxwriter

# Sample DataFrame with NaN and inf values
data = {
    'A': [1, 2, np.nan, 4, np.inf],
    'B': [np.inf, 3, 4, np.nan, 6],
    'C': [7, 8, 9, 10, 11]
}

df = pd.DataFrame(data)

# Function to replace NaN and inf values
def replace_invalid_values(value):
    if pd.isna(value):
        return 'NaN'
    elif value == np.inf:
        return 'Inf'
    elif value == -np.inf:
        return '-Inf'
    else:
        return value

# Apply the function to the DataFrame
df_cleaned = df.applymap(replace_invalid_values)

# Write to Excel using xlsxwriter
with pd.ExcelWriter('output.xlsx', engine='xlsxwriter') as writer:
    df_cleaned.to_excel(writer, index=False, sheet_name='Sheet1')

print("Excel file created successfully.")
