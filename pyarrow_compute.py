import pyarrow as pa
import pyarrow.csv as pv
import pyarrow.compute as pc

def convert_date_column(column, format_str):
    return pc.strptime(column, format=format_str, unit='s')

def convert_numeric_column(column):
    return pc.cast(column, pa.float64())

def read_and_convert_csv(file_path):
    # Read the CSV file
    table = pv.read_csv(file_path)
    
    # Define conversions
    conversions = {
        'date_column1': {'type': 'date', 'format': '%Y-%m-%d'},
        'date_column2': {'type': 'date', 'format': '%d/%m/%Y'},
        'numeric_column1': {'type': 'numeric'},
        'numeric_column2': {'type': 'numeric'},
    }

    # Apply conversions
    for column_name, conversion_info in conversions.items():
        if column_name in table.schema.names:
            column = table[column_name]
            
            if conversion_info['type'] == 'date':
                converted_column = convert_date_column(column, conversion_info['format'])
            elif conversion_info['type'] == 'numeric':
                converted_column = convert_numeric_column(column)
            else:
                raise ValueError(f"Unsupported conversion type: {conversion_info['type']}")
            
            table = table.set_column(table.schema.get_field_index(column_name), column_name, converted_column)

    # Inspect the new schema
    print("New Schema:")
    print(table.schema)
    
    return table

# Example usage
file_path = 'your_file.csv'
new_table = read_and_convert_csv(file_path)
print(new_table)
