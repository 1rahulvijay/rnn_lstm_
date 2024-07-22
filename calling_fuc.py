class Calculator:
    def __init__(self, operand1, operand2):
        self.operand1 = operand1
        self.operand2 = operand2
    
    def add(self, operand3=0, operand4=0):
        result = self.operand1 + self.operand2 + operand3 + operand4
        print(f"Addition: {self.operand1} + {self.operand2} + {operand3} + {operand4} = {result}")
        return result
    
    def subtract(self, operand3=0, operand4=0):
        result = self.operand1 - self.operand2 - operand3 - operand4
        print(f"Subtraction: {self.operand1} - {self.operand2} - {operand3} - {operand4} = {result}")
        return result
    
    def multiply(self, operand3=1, operand4=1):
        result = self.operand1 * self.operand2 * operand3 * operand4
        print(f"Multiplication: {self.operand1} * {self.operand2} * {operand3} * {operand4} = {result}")
        return result
    
    def divide(self, operand3=1, operand4=1):
        if self.operand2 == 0 or operand3 == 0 or operand4 == 0:
            print("Division by zero is not allowed.")
            return None
        result = self.operand1 / self.operand2 / operand3 / operand4
        print(f"Division: {self.operand1} / {self.operand2} / {operand3} / {operand4} = {result}")
        return result
    
    def modulus(self, operand3=1, operand4=1):
        result = self.operand1 % self.operand2 % operand3 % operand4
        print(f"Modulus: {self.operand1} % {self.operand2} % {operand3} % {operand4} = {result}")
        return result
    
    def run_operations(self, operations_to_run, **kwargs):
        for operation_name in operations_to_run:
            method = getattr(self, operation_name, None)
            if callable(method):
                # Default values for operand3 and operand4
                operand3 = kwargs.get('operand3', 0)
                operand4 = kwargs.get('operand4', 0)
                method(operand3, operand4)
            else:
                print(f"{operation_name} is not a valid operation")

# Create an instance of the Calculator class
calculator = Calculator(10, 5)

# Define the list of operations to call
all_operations = ["add", "subtract", "multiply", "divide", "modulus"]
subset_operations = ["add", "multiply", "modulus"]

# Call all operations with specific parameters
print("Calling all operations with specified parameters:\n")
calculator.run_operations(all_operations, operand3=2, operand4=3)

print("\nCalling only specific operations with specified parameters:\n")
calculator.run_operations(subset_operations, operand3=4, operand4=5)
