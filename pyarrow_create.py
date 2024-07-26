import pyarrow as pa
import pandas as pd

# Step 1: Create a Pandas DataFrame and convert to PyArrow Table
data = {
    'column1': ['short', 'medium_length', 'a_very_long_value_here'],
    'column2': ['value4', 'value5', 'value6'],
    'column3': ['value7', 'value8', 'a_really_long_value_exceeding']
}

df = pd.DataFrame(data)
table = pa.Table.from_pandas(df)

# Step 2: Determine the maximum length of data for each column
def get_max_length_per_column(table):
    max_lengths = {}
    
    for col in table.column_names:
        # Extract column data as a list
        col_data = table.column(col).to_pylist()
        
        # Find the maximum length of strings in this column
        max_length = max((len(str(value)) for value in col_data), default=0)
        
        max_lengths[col] = max_length
    
    return max_lengths

max_lengths = get_max_length_per_column(table)
print("Max lengths:", max_lengths)

# Step 3: Generate the CREATE TABLE query
def generate_create_table_query(table, table_name):
    # Get maximum lengths for VARCHAR columns
    max_lengths = get_max_length_per_column(table)
    
    # Generate column definitions with VARCHAR lengths
    columns_definitions = []
    for col, max_length in max_lengths.items():
        columns_definitions.append(f"{col} VARCHAR({max_length})")
    
    columns_str = ', '.join(columns_definitions)
    
    # Create the final CREATE TABLE query
    query = f"CREATE TABLE {table_name} ({columns_str});"
    return query

# Define the table name
table_name = 'your_table_name'

# Generate the CREATE TABLE query
create_table_query = generate_create_table_query(table, table_name)
print(create_table_query)
