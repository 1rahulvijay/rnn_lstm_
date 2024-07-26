import pandas as pd
import pyarrow as pa

# Step 1: Create a Pandas DataFrame and convert to PyArrow Table
data = {
    'column1': ['value1', 'value2', 'value3'],
    'column2': ['value4', 'value5', 'value6'],
    'column3': ['value7', 'value8', 'value9']
}

df = pd.DataFrame(data)
table = pa.Table.from_pandas(df)

# Step 2: Generate the SQL INSERT query directly from PyArrow Table
def generate_insert_query_from_pyarrow_table(table, table_name):
    # Convert PyArrow Table to Pandas DataFrame
    df = table.to_pandas()
    
    # Extract column names
    columns = df.columns
    
    # Generate column part of the query
    columns_str = ', '.join(columns)
    
    # Generate values part of the query
    values_list = []
    for row in df.itertuples(index=False, name=None):
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
