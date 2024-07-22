import pandas as pd

# Sample DataFrame
data = {
    'col1': ['short', 'medium_length', 'longest_string_in_dataframe'],
    'col2': ['a', 'aa', 'aaa'],
    # Add more columns as needed
}

df = pd.DataFrame(data)

# Function to calculate the maximum length of each string column
def calculate_max_lengths(df, buffer=10):
    max_lengths = {}
    for col in df.select_dtypes(include=[object]):
        max_length = df[col].map(len).max()
        max_lengths[col] = max_length + buffer
    return max_lengths

# Calculate the maximum lengths with a buffer
max_lengths = calculate_max_lengths(df, buffer=20)

# Generate the CREATE TABLE query
def generate_create_table_query(table_name, df, max_lengths):
    query = f"CREATE TABLE {table_name} (\n"
    for col in df.columns:
        if df[col].dtype == 'object':
            col_type = f"VARCHAR({max_lengths[col]})"
        elif pd.api.types.is_integer_dtype(df[col]):
            col_type = "INT"
        elif pd.api.types.is_float_dtype(df[col]):
            col_type = "FLOAT"
        else:
            col_type = "TEXT"  # Default to TEXT for any other types
        query += f"  {col} {col_type},\n"
    query = query.rstrip(',\n') + "\n);"
    return query

# Generate and print the query
table_name = 'your_table_name'
create_table_query = generate_create_table_query(table_name, df, max_lengths)
print(create_table_query)
