import pandas as pd

# Assuming you have an existing DataFrame
df = pd.DataFrame({'Name': ['John', 'Alice'], 'Age': [25, 30]})

# Create a new row as a dictionary
new_row = {'Name': 'Bob', 'Age': 28}

# Append the new row to the DataFrame
df = df._append(new_row, ignore_index=True)

# Print the updated DataFrame
print(df)
