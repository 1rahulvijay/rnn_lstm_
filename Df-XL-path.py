import os
import pandas as pd

class DataFrameHandler:
    def __init__(self, input_data, sheet_name=None, file_extensions=None):
        self.raw_input = input_data
        self.sheet_name = sheet_name
        self.file_extensions = file_extensions if file_extensions else ['.csv']
        self.df = self._initialize_data(input_data)

    def _initialize_data(self, input_data):
        if isinstance(input_data, pd.DataFrame):
            return input_data
        elif isinstance(input_data, str):
            if os.path.isfile(input_data):
                return self._read_file(input_data)
            elif os.path.isdir(input_data):
                return self._read_directory(input_data)
            else:
                raise ValueError("Provided string is neither a file path nor a directory.")
        else:
            raise ValueError("Input should be a pandas DataFrame, a file path, or a directory path.")

    def _read_file(self, file_path):
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            return pd.read_excel(file_path, sheet_name=self.sheet_name)
        else:
            raise ValueError("Unsupported file format. Only CSV and Excel files are supported.")

    def _read_directory(self, directory_path):
        all_dfs = []
        for file_name in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file_name)
            if os.path.isfile(file_path) and any(file_path.endswith(ext) for ext in self.file_extensions):
                df = self._read_file(file_path)
                all_dfs.append(df)
        if all_dfs:
            return pd.concat(all_dfs, ignore_index=True)
        else:
            raise ValueError("No valid files found in the directory.")

    def get_raw_input(self):
        return self.raw_input

    def get_data(self):
        return self.df

    def perform_action(self, action, *args, **kwargs):
        if hasattr(self.df, action):
            method = getattr(self.df, action)
            return method(*args, **kwargs)
        else:
            raise ValueError(f"DataFrame has no method called {action}")

# Example usage
if __name__ == "__main__":
    # Example DataFrame
    data = {'col1': [1, 2], 'col2': [3, 4]}
    df = pd.DataFrame(data)
    
    # Initializing with a DataFrame
    handler = DataFrameHandler(df)
    print("Raw Input DataFrame:")
    print(handler.get_raw_input())
    print("Processed DataFrame:")
    print(handler.get_data().head())

    # Initializing with a CSV file path
    handler = DataFrameHandler('path/to/your/file.csv')
    print("Raw Input Path:")
    print(handler.get_raw_input())
    print("Processed DataFrame:")
    print(handler.get_data().head())

    # Initializing with an Excel file path and specifying sheet name
    handler = DataFrameHandler('path/to/your/file.xlsx', sheet_name='Sheet1')
    print("Raw Input Path:")
    print(handler.get_raw_input())
    print("Processed DataFrame:")
    print(handler.get_data().head())

    # Initializing with a directory path and specifying file extensions
    handler = DataFrameHandler('path/to/your/directory', file_extensions=['.csv', '.xlsx'])
    print("Raw Input Directory Path:")
    print(handler.get_raw_input())
    print("Processed DataFrame:")
    print(handler.get_data().head())
