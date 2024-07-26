import pandas as pd
import pyarrow as pa

# Step 1: Create a Pandas DataFrame
data = {
    'column1': ['value1', 'value2', 'value3'],
    'column2': ['value4', 'value5', 'value6'],
    'column3': ['value7', 'value8', 'value9']
}

df = pd.DataFrame(data)

# Step 2: Convert Pandas DataFrame to PyArrow Table
table = pa.Table.from_pandas(df)

# Step 3: Generate the SQL INSERT query directly from PyArrow Table
def generate_insert_query_from_pyarrow_table(table, table_name):
    # Extract column names
    columns = table.column_names
    
    # Generate column part of the query
    columns_str = ', '.join(columns)
    
    # Generate values part of the query
    values_list = []
    for i in range(table.num_rows):
        row = tuple(table.column(col).as_py(i) for col in columns)
        values_list.append(str(row))
    
    values_str = ', '.join(values_list)
    
    # Create the final query
    query = f"INSERT INTO {table_name} ({columns_str}) VALUES {values_str};"
    return query

# Define the table name
table_name = 'your_table_name'

# Generate the query
query = generate_insert_query_from_pyarrow_table(table, table_name)
print(query)
