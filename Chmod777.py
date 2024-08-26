import csv

# Specify the columns you want to exclude
exclude_columns = ['Column1', 'Column2']

# Read the CSV file
with open('your_file.csv', mode='r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    
    # Create a list of fieldnames excluding the columns you want to remove
    fieldnames = [field for field in reader.fieldnames if field not in exclude_columns]
    
    # Process the rows with filtered columns
    for row in reader:
        filtered_row = {key: value for key, value in row.items() if key not in exclude_columns}
        # Do something with filtered_row
        print(filtered_row)
