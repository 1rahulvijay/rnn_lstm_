mport pyarrow.csv as pv
import pyarrow as pa

# Path to your CSV file
csv_file_path = 'path/to/your/file.csv'

# Define read options
read_options = pv.ReadOptions(
    use_threads=True,  # Use multiple threads for reading
    skip_rows=0,       # Number of rows to skip at the start of the file
    column_names=['col1', 'col2', 'col3']  # Specify column names if the CSV doesn't have a header
)

# Define parse options
parse_options = pv.ParseOptions(
    delimiter=',',     # Specify the delimiter
    quote_char='"',    # Specify the quote character
    double_quote=True, # Allow double quotes
    escape_char=None,  # Escape character
    newlines_in_values=False, # Allow newlines in values
    header_rows=1      # Specify number of header rows
)

# Read the CSV file into a PyArrow Table with specified options
table = pv.read_csv(csv_file_path, read_options=read_options, parse_options=parse_options)

# Show the table
print(table)

# Convert the PyArrow Table to a dictionary
data_dict = table.to_pydict()
print(data_dict)

# Access specific columns (as PyArrow Arrays)
column_name = 'col1'
column_data = table[column_name]
print(column_data)
