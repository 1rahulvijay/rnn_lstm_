import pandas as pd
import pyarrow as pa

# Step 1: Create a Pandas DataFrame and convert to PyArrow Table
data = {
    'column1': ['2024-01-01', '2024-02-01', '2024-03-01'],  # Dates as strings
    'column2': ['value4', 'value5', 'value6'],  # Strings
    'column3': [1.23, 4.56, 7.89],  # Float
    'column4': [pd.Timestamp('2024-01-01 12:00:00'), pd.Timestamp('2024-02-01 12:00:00'), pd.Timestamp('2024-03-01 12:00:00')]  # Timestamps
}

df = pd.DataFrame(data)
table = pa.Table.from_pandas(df)

# Step 2: Determine the maximum length of data for VARCHAR columns
def get_max_length_per_column(table):
    max_lengths = {}
    
    for col in table.column_names:
        col_data = table.column(col).to_pylist()
        
        if isinstance(col_data[0], str):
            max_length = max((len(str(value)) for value in col_data), default=0)
            max_lengths[col] = max_length
    
    return max_lengths

# Step 3: Determine SQL data type based on PyArrow column type
def get_sql_data_type(column):
    if pa.types.is_timestamp(column.type):
        return 'TIMESTAMP'
    elif pa.types.is_date(column.type):
        return 'DATE'
    elif pa.types.is_string(column.type):
        return 'VARCHAR'
    elif pa.types.is_floating(column.type):
        return 'FLOAT'
    elif pa.types.is_integer(column.type):
        return 'INTEGER'
    else:
        return 'TEXT'  # Default case for unknown types

# Step 4: Generate the CREATE TABLE query
def generate_create_table_query(table, table_name):
    max_lengths = get_max_length_per_column(table)
    
    columns_definitions = []
    for col in table.column_names:
        column = table.column(col)
        sql_type = get_sql_data_type(column)
        
        if sql_type == 'VARCHAR':
            max_length = max_lengths.get(col, 255)
            column_definition = f"{col} VARCHAR({max_length})"
        else:
            column_definition = f"{col} {sql_type}"
        
        columns_definitions.append(column_definition)
    
    columns_str = ', '.join(columns_definitions)
    query = f"CREATE TABLE {table_name} ({columns_str});"
    return query

# Define the table name
table_name = 'your_table_name'

# Generate the CREATE TABLE query
create_table_query = generate_create_table_query(table, table_name)
print(create_table_query)
