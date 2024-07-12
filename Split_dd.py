import pandas as pd

def split_dataframe_by_category(df, categories):
    # Group by 'Category' column
    grouped = df.groupby('Category')

    # Create a dictionary to hold the resulting DataFrames
    dfs = {category: group.copy() for category, group in grouped}

    # Extract the DataFrames for each specified category
    result = {category: dfs.get(category, pd.DataFrame()) for category in categories}

    return result

# Example usage:
data = {
    'Category': ['A', 'B', 'A', 'C', 'B', 'A'],
    'Value': [10, 20, 30, 40, 50, 60]
}
df = pd.DataFrame(data)
categories = ['A', 'B', 'C', 'D']  # Assuming you want to check for categories A, B, C, and D

dfs = split_dataframe_by_category(df, categories)

for category in categories:
    print(f"DataFrame for Category {category}:")
    print(dfs[category])
    print()
