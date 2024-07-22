import pandas as pd

class Calculator:
    def __init__(self, operand1, operand2):
        self.operand1 = operand1
        self.operand2 = operand2
    
    def add(self, operand3=0, operand4=0):
        result = self.operand1 + self.operand2 + operand3 + operand4
        data = {
            'Operation': ['Addition'],
            'Operand1': [self.operand1],
            'Operand2': [self.operand2],
            'Operand3': [operand3],
            'Operand4': [operand4],
            'Result': [result]
        }
        return pd.DataFrame(data)
    
    def subtract(self, operand3=0, operand4=0):
        result = self.operand1 - self.operand2 - operand3 - operand4
        data = {
            'Operation': ['Subtraction'],
            'Operand1': [self.operand1],
            'Operand2': [self.operand2],
            'Operand3': [operand3],
            'Operand4': [operand4],
            'Result': [result]
        }
        return pd.DataFrame(data)
    
    def multiply(self, operand3=1, operand4=1):
        result = self.operand1 * self.operand2 * operand3 * operand4
        data = {
            'Operation': ['Multiplication'],
            'Operand1': [self.operand1],
            'Operand2': [self.operand2],
            'Operand3': [operand3],
            'Operand4': [operand4],
            'Result': [result]
        }
        return pd.DataFrame(data)
    
    def divide(self, operand3=1, operand4=1):
        if self.operand2 == 0 or operand3 == 0 or operand4 == 0:
            print("Division by zero is not allowed.")
            return pd.DataFrame()
        result = self.operand1 / self.operand2 / operand3 / operand4
        data = {
            'Operation': ['Division'],
            'Operand1': [self.operand1],
            'Operand2': [self.operand2],
            'Operand3': [operand3],
            'Operand4': [operand4],
            'Result': [result]
        }
        return pd.DataFrame(data)
    
    def modulus(self, operand3=1, operand4=1):
        result = self.operand1 % self.operand2 % operand3 % operand4
        data = {
            'Operation': ['Modulus'],
            'Operand1': [self.operand1],
            'Operand2': [self.operand2],
            'Operand3': [operand3],
            'Operand4': [operand4],
            'Result': [result]
        }
        return pd.DataFrame(data)
    
    def run_operations(self, operations_to_run, **kwargs):
        dataframes = []
        for operation_name in operations_to_run:
            method = getattr(self, operation_name, None)
            if callable(method):
                # Default values for operand3 and operand4
                operand3 = kwargs.get('operand3', 0)
                operand4 = kwargs.get('operand4', 0)
                df = method(operand3, operand4)
                if not df.empty:
                    dataframes.append((operation_name, df))
            else:
                print(f"{operation_name} is not a valid operation")
        return dataframes

# Create an instance of the Calculator class
calculator = Calculator(10, 5)

# Define the list of operations to call
all_operations = ["add", "subtract", "multiply", "divide", "modulus"]
subset_operations = ["add", "multiply", "modulus"]

# Call all operations with specific parameters
print("Calling all operations with specified parameters:\n")
dataframes = calculator.run_operations(all_operations, operand3=2, operand4=3)

# Write the DataFrames to an Excel file with multiple sheets
with pd.ExcelWriter("calculator_results.xlsx") as writer:
    for operation_name, df in dataframes:
        df.to_excel(writer, sheet_name=operation_name, index=False)

print("\nResults have been written to 'calculator_results.xlsx'")
