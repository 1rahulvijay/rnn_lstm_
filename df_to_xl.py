import pandas as pd

def dataframes_to_excel(dataframes, sheet_names, file_name):
    """
    Writes multiple DataFrames to an Excel file, each DataFrame in a different sheet.
    
    :param dataframes: List of pandas DataFrames to write to Excel.
    :param sheet_names: List of sheet names corresponding to the DataFrames.
    :param file_name: The name of the output Excel file.
    """
    with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:
        for dataframe, sheet_name in zip(dataframes, sheet_names):
            dataframe.to_excel(writer, sheet_name=sheet_name, index=False)

# Example usage:
df1 = pd.DataFrame({'Column1': [1, 2], 'Column2': [3, 4]})
df2 = pd.DataFrame({'ColumnA': ['A', 'B'], 'ColumnB': ['C', 'D']})

dataframes = [df1, df2]
sheet_names = ['Sheet1', 'Sheet2']
file_name = 'output.xlsx'

dataframes_to_excel(dataframes, sheet_names, file_name)
