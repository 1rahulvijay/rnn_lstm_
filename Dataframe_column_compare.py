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
    - A dictionary with comparison results and detailed match statements
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
    missing_in_df = oracle_columns_set - df_columns_set
    extra_in_df = df_columns_set - oracle_columns_set

    if not missing_in_df and not extra_in_df:
        statement = "All columns match between the DataFrame and the Oracle table."
    else:
        statement = "Columns do not match between the DataFrame and the Oracle table."

    result = {
        'match': not missing_in_df and not extra_in_df,
        'statement': statement,
        'missing_in_df': list(missing_in_df),
        'extra_in_df': list(extra_in_df)
    }

    return result

# Example usage:
import cx_Oracle

# Create your DataFrame
df = pd.DataFrame({
    # Your DataFrame data here
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

# Print results
print(comparison_result['statement'])
if not comparison_result['match']:
    print(f"Missing in DataFrame: {comparison_result['missing_in_df']}")
    print(f"Extra in DataFrame: {comparison_result['extra_in_df']}")
