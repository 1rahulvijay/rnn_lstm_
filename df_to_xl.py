import pandas as pd

# Sample DataFrame including an empty column 'EmptyColumn'
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'Score': [85.5, 90.0, 95.5],
    'EmptyColumn': [None, None, None]  # Empty column
})

# Create a pandas Excel writer using XlsxWriter as the engine
writer = pd.ExcelWriter('styled_output.xlsx', engine='xlsxwriter')
df.to_excel(writer, index=False, sheet_name='Sheet1')

# Access the workbook and the worksheet
workbook = writer.book
worksheet = writer.sheets['Sheet1']

# Define the default style for data cells
data_format = workbook.add_format({
    'font_name': 'Calibri',
    'font_size': 11,
    'bold': False,
    'font_color': 'black',
    'bg_color': '#FFFFCC',
    'align': 'center',
    'valign': 'vcenter'
})

# Define the style for header cells
header_format = workbook.add_format({
    'font_name': 'Calibri',
    'font_size': 12,
    'bold': True,
    'font_color': 'white',
    'bg_color': '#4F81BD',
    'align': 'center',
    'valign': 'vcenter'
})

# Apply the header style to the header row
for col_num, value in enumerate(df.columns.values):
    worksheet.write(0, col_num, value, header_format)

# Apply the data style to all data cells
for row_num in range(1, len(df) + 1):
    for col_num in range(len(df.columns)):
        worksheet.write(row_num, col_num, df.iloc[row_num - 1, col_num], data_format)

# Adjust column widths
for col_num, column in enumerate(df.columns):
    # Set a minimum width to handle empty columns
    max_len = max(df[column].astype(str).map(len).max() if not df[column].isnull().all() else 0, len(column)) + 2
    worksheet.set_column(col_num, col_num, max_len)

# Ensure that even empty columns are visible by setting a default width
empty_col_min_width = 15  # Minimum width for empty columns
for col_num, column in enumerate(df.columns):
    if df[column].isnull().all():
        worksheet.set_column(col_num, col_num, empty_col_min_width, data_format)

# Save the workbook
writer.save()
