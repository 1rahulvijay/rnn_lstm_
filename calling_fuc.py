class Calculator:
    def __init__(self, operand1, operand2):
        self.operand1 = operand1
        self.operand2 = operand2
    
    def add(self):
        result = self.operand1 + self.operand2
        print(f"Addition: {self.operand1} + {self.operand2} = {result}")
        return result
    
    def subtract(self):
        result = self.operand1 - self.operand2
        print(f"Subtraction: {self.operand1} - {self.operand2} = {result}")
        return result
    
    def multiply(self):
        result = self.operand1 * self.operand2
        print(f"Multiplication: {self.operand1} * {self.operand2} = {result}")
        return result
    
    def divide(self):
        if self.operand2 == 0:
            print("Division by zero is not allowed.")
            return None
        result = self.operand1 / self.operand2
        print(f"Division: {self.operand1} / {self.operand2} = {result}")
        return result
    
    def modulus(self):
        result = self.operand1 % self.operand2
        print(f"Modulus: {self.operand1} % {self.operand2} = {result}")
        return result
    
    def run_operations(self, operations_to_run):
        for operation_name in operations_to_run:
            method = getattr(self, operation_name, None)
            if callable(method):
                method()
            else:
                print(f"{operation_name} is not a valid operation")

# Create an instance of the Calculator class
calculator = Calculator(10, 5)

# Define the list of operations to call
all_operations = ["add", "subtract", "multiply", "divide", "modulus"]
subset_operations = ["add", "multiply", "modulus"]

# Call all operations
print("Calling all operations:\n")
calculator.run_operations(all_operations)

print("\nCalling only specific operations:\n")

# Call only specific operations (e.g., add, multiply, and modulus)
calculator.run_operations(subset_operations)
