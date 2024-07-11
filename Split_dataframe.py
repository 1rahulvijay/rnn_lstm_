# Group by 'Category' column
grouped = df.groupby('Category')

# Create a dictionary to hold the resulting DataFrames
dfs = {category: group.copy() for category, group in grouped}

# Now you have a dictionary with DataFrames for each category
df_A = dfs['A']
df_B = dfs['B']
df_C = dfs['C']

print("DataFrame for Category A:")
print(df_A)
print
