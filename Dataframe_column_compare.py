import pandas as pd

def compare_columns(cursor, df, schema_name, table_name):
    """
    Compare DataFrame column names with Oracle table column names.

    Parameters:
    - cursor: cx_Oracle cursor object
    - df: pandas DataFrame
    - schema_name: str, Oracle schema name (case-insensitive)
    - table_name: str, name of the Oracle table (case-insensitive)

    Returns:
    - A dictionary with comparison results including whether all columns match (True/False),
      and detailed information on matched, missing, and extra columns.
    """
    # Fetch column names from Oracle table
    cursor.execute("""
        SELECT COLUMN_NAME 
        FROM ALL_TAB_COLUMNS 
        WHERE TABLE_NAME = :table_name
        AND OWNER = :schema_name
    """, table_name=table_name.upper(), schema_name=schema_name.upper())

    oracle_columns = [row[0] for row in cursor.fetchall()]

    # Normalize column names by converting to uppercase
    df_columns_set = set(col.upper() for col in df.columns)
    oracle_columns_set = set(col.upper() for col in oracle_columns)

    # Compare the sets
    matched_columns = df_columns_set & oracle_columns_set
    missing_in_df = oracle_columns_set - df_columns_set
    extra_in_df = df_columns_set - oracle_columns_set

    match = not missing_in_df and not extra_in_df
    
    # Print the results
    print("Matched columns:")
    print(matched_columns if matched_columns else "None")
    print("\nMissing in DataFrame:")
    print(missing_in_df if missing_in_df else "None")
    print("\nExtra in DataFrame:")
    print(extra_in_df if extra_in_df else "None")
    
    # Return detailed information and match status
    result = {
        'match': match,
        'matched_columns': list(matched_columns),
        'missing_in_df': list(missing_in_df),
        'extra_in_df': list(extra_in_df)
    }

    return result

# Example usage:
import cx_Oracle

# Create your DataFrame
df = pd.DataFrame({
    # Your DataFrame data here
    'column1': [],
    'column2': [],
    # Add columns as needed
})

# Connect to Oracle and create cursor
conn = cx_Oracle.connect('user/password@host:port/service_name')
cursor = conn.cursor()

# Define schema and table names
schema_name = 'YOUR_SCHEMA_NAME'
table_name = 'YOUR_TABLE_NAME'

# Compare columns
comparison_result = compare_columns(cursor, df, schema_name, table_name)

# Close cursor and connection
cursor.close()
conn.close()

# Print whether all columns match or not
if comparison_result['match']:
    print("\nAll columns match between the DataFrame and the Oracle table.")
else:
    print("\nColumns do not match between the DataFrame and the Oracle table.")
