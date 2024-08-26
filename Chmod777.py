import pandas as pd

# Sample DataFrame
data = {'A': ['apple', 'banana', 'cherry'], 'B': ['dog', 'elephant', 'frog'], 'C': ['hat', 'igloo', 'jacket']}
df = pd.DataFrame(data)

# Value to search
value_to_search = 'banana'

# Find columns containing the value
columns_with_value = df.columns[df.isin([value_to_search]).any()]

print(columns_with_value)
