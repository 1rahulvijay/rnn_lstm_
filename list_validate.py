import cx_Oracle

class DataValidator:
    def __init__(self, parameter_rules):
        # Initialize with parameter validation rules
        self.rules = parameter_rules

    def validate(self, data):
        errors = []
        for params in data:
            for idx, value in enumerate(params):
                key = f'param{idx + 1}'
                if key in self.rules:
                    rule = self.rules[key]
                    value_type = rule.get('type')
                    max_length = rule.get('max_length')
                    min_value = rule.get('min_value')
                    max_value = rule.get('max_value')

                    # Check type
                    if not isinstance(value, value_type):
                        errors.append(f"{key.capitalize()} must be of type {value_type.__name__}")

                    # Check length (if applicable)
                    if isinstance(value, str) and max_length and len(value) > max_length:
                        errors.append(f"{key.capitalize()} must be {max_length} characters or fewer")

                    # Check numeric value range (if applicable)
                    if isinstance(value, int):
                        if min_value and value < min_value:
                            errors.append(f"{key.capitalize()} must be at least {min_value}")
                        if max_value and value > max_value:
                            errors.append(f"{key.capitalize()} must be at most {max_value}")

                    # Add more specific checks based on your requirements

        return errors

# Function to insert data into Oracle database
def insert_data(conn, data):
    try:
        cursor = conn.cursor()

        # Validate data
        validator = DataValidator({
            'param1': {'type': int},
            'param2': {'type': str, 'max_length': 50},
            'param3': {'type': str, 'max_length': 50},
            'param4': {'type': str, 'max_length': 50}
            # Add more parameters as needed
        })
        validation_errors = validator.validate(data)
        if validation_errors:
            print("Data validation failed:")
            for error in validation_errors:
                print(f"- {error}")
            return False

        # Insert data into database (example assumes a table called 'your_table')
        for params in data:
            cursor.execute("INSERT INTO your_table (column1, column2, column3, column4) VALUES (:1, :2, :3, :4)", params)
        conn.commit()
        print("Data inserted successfully.")
        return True

    except cx_Oracle.Error as e:
        print(f"Database error: {e}")
        return False

    finally:
        if conn:
            conn.close()

# Main function for interactive data input and insertion
def main():
    conn = None
    try:
        # Connect to Oracle database
        conn = cx_Oracle.connect('username/password@hostname/service_name')

        # Example data list (each item is a tuple with parameters)
        data = [(1, 'b', 'f', 'j')]

        # Insert data into database
        insert_data(conn, data)

    except cx_Oracle.Error as e:
        print(f"Database error: {e}")

    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

# Entry point of the script
if __name__ == "__main__":
    main()
