import os
import pandas as pd

class DataFrameHandler:
    def __init__(self, input_data, params=None):
        self.raw_input = input_data
        self.params = params if params else {}
        self.file_extensions = self.params.get('file_extensions', ['.csv', '.xlsx'])
        self.file_specific_params = self.params.get('file_specific_params', {})
        self.concat_dataframes = self.params.get('concat_dataframes', True)
        self.additional_columns = self.params.get('additional_columns', {})
        self.dfs = self._initialize_data(input_data)

    def _initialize_data(self, input_data):
        if isinstance(input_data, pd.DataFrame):
            df = input_data
            self._add_additional_columns(df, 'default')
            return [df] if not self.concat_dataframes else df
        elif isinstance(input_data, str):
            if os.path.isfile(input_data):
                df = self._read_file(input_data)
                self._add_additional_columns(df, os.path.basename(input_data))
                return [df] if not self.concat_dataframes else df
            elif os.path.isdir(input_data):
                return self._read_directory(input_data)
            else:
                raise ValueError("Provided string is neither a file path nor a directory.")
        else:
            raise ValueError("Input should be a pandas DataFrame, a file path, or a directory path.")

    def _read_file(self, file_path):
        file_name = os.path.basename(file_path)
        file_params = self.file_specific_params.get(file_name, {})
        
        if file_path.endswith('.csv'):
            df = pd.read_csv(
                file_path, 
                header=file_params.get('header', 0), 
                usecols=file_params.get('usecols', None)
            )
        elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            df = pd.read_excel(
                file_path, 
                sheet_name=file_params.get('sheet_name', None), 
                header=file_params.get('header', 0), 
                usecols=file_params.get('usecols', None)
            )
        else:
            raise ValueError("Unsupported file format. Only CSV and Excel files are supported.")
        
        return df

    def _read_directory(self, directory_path):
        all_dfs = []
        for file_name in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file_name)
            if os.path.isfile(file_path) and any(file_path.endswith(ext) for ext in self.file_extensions):
                df = self._read_file(file_path)
                self._add_additional_columns(df, file_name)
                all_dfs.append(df)
        if not all_dfs:
            raise ValueError("No valid files found in the directory.")
        return pd.concat(all_dfs, ignore_index=True) if self.concat_dataframes else all_dfs

    def _add_additional_columns(self, df, file_name):
        additional_cols = self.additional_columns.get(file_name, self.additional_columns.get('default', {}))
        if additional_cols:
            for col_name, col_value in additional_cols.items():
                df[col_name] = col_value

    def get_raw_input(self):
        return self.raw_input

    def get_data(self):
        return self.dfs if not self.concat_dataframes else self.dfs

    def perform_action(self, action, *args, **kwargs):
        if self.concat_dataframes:
            if hasattr(self.dfs, action):
                method = getattr(self.dfs, action)
                return method(*args, **kwargs)
            else:
                raise ValueError(f"DataFrame has no method called {action}")
        else:
            results = []
            for df in self.dfs:
                if hasattr(df, action):
                    method = getattr(df, action)
                    results.append(method(*args, **kwargs))
                else:
                    raise ValueError(f"DataFrame has no method called {action}")
            return results

    def __call__(self):
        if self.concat_dataframes:
            return self.dfs
        else:
            return self.dfs[0] if self.dfs else None

# Example usage
if __name__ == "__main__":
    # Example DataFrame
    data = {'col1': [1, 2], 'col2': [3, 4]}
    df = pd.DataFrame(data)
    
    # Initializing with a DataFrame
    handler = DataFrameHandler(df, params={
        'concat_dataframes': False,
        'additional_columns': {
            'default': {'extra_col1': 1, 'extra_col2': 2}
        }
    })
    print("Raw Input DataFrame:")
    print(handler.get_raw_input())
    print("Processed DataFrames:")
    for dataframe in handler.get_data():
        print(dataframe.head())
    print("Returned DataFrame:")
    print(handler())

    # Initializing with a CSV file path
    handler = DataFrameHandler('path/to/your/file.csv', params={
        'concat_dataframes': False,
        'additional_columns': {
            'file.csv': {'extra_col1': 1, 'extra_col2': 2}
        }
    })
    print("Raw Input Path:")
    print(handler.get_raw_input())
    print("Processed DataFrames:")
    for dataframe in handler.get_data():
        print(dataframe.head())
    print("Returned DataFrame:")
    print(handler())

    # Initializing with an Excel file path and specifying sheet name and header
    params = {
        'sheet_name': 'Sheet1',
        'header': 0,
        'concat_dataframes': False,
        'additional_columns': {
            'file.xlsx': {'extra_col1': 1, 'extra_col2': 2}
        }
    }
    handler = DataFrameHandler('path/to/your/file.xlsx', params=params)
    print("Raw Input Path:")
    print(handler.get_raw_input())
    print("Processed DataFrames:")
    for dataframe in handler.get_data():
        print(dataframe.head())
    print("Returned DataFrame:")
    print(handler())

    # Initializing with a directory path and specifying file-specific parameters, including additional columns
    file_specific_params = {
        'file1.csv': {'header': 0, 'usecols': ['col1', 'col2']},
        'file2.xlsx': {'sheet_name': 'Sheet1', 'header': 0, 'usecols': ['col1', 'col2']},
        'file3.xlsx': {'sheet_name': 'Sheet2', 'header': 0, 'usecols': ['col1', 'col2']},
        'file4.xlsx': {'sheet_name': 'Sheet3', 'header': 0, 'usecols': ['col1', 'col2']}
    }
    params = {
        'file_extensions': ['.csv', '.xlsx'],
        'file_specific_params': file_specific_params,
        'concat_dataframes': False,
        'additional_columns': {
            'file1.csv': {'extra_col1': 1, 'extra_col2': 2},
            'file2.xlsx': {'extra_col1': 3, 'extra_col2': 4},
            'file3.xlsx': {'extra_col1': 5, 'extra_col2': 6},
            # 'file4.xlsx' will have no additional columns as it is not specified in additional_columns
            'default': {'extra_col1': 0, 'extra_col2': 0}  # default columns for files not specifically mentioned
        }
    }
    handler = DataFrameHandler('path/to/your/directory', params=params)
    print("Raw Input Directory Path:")
    print(handler.get_raw_input())
    print("Processed DataFrames:")
    for dataframe in handler.get_data():
        print(dataframe.head())
    print("Returned DataFrame:")
    print(handler())
