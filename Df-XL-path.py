import os
import pandas as pd

class DataFrameHandler:
    def __init__(self, input_data):
        if isinstance(input_data, pd.DataFrame):
            self.df = input_data
        elif isinstance(input_data, str):
            if os.path.isfile(input_data):
                self.df = pd.read_csv(input_data)
            elif os.path.isdir(input_data):
                self.df = self._read_directory(input_data)
            else:
                raise ValueError("Provided string is neither a file path nor a directory.")
        else:
            raise ValueError("Input should be a pandas DataFrame, a file path, or a directory path.")

    def _read_directory(self, directory_path):
        all_dfs = []
        for file_name in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file_name)
            if os.path.isfile(file_path) and file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
                all_dfs.append(df)
        return pd.concat(all_dfs, ignore_index=True)

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
    print(handler.perform_action('head'))

    # Initializing with a file path
    handler = DataFrameHandler('path/to/your/file.csv')
    print(handler.perform_action('head'))

    # Initializing with a directory path
    handler = DataFrameHandler('path/to/your/directory')
    print(handler.perform_action('head'))
