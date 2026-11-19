
import pandas as pd
import openpyxl
from dotenv import load_dotenv
import numpy as np

print("Pandas version:", pd.__version__)
print("Openpyxl version:", openpyxl.__version__)
print("Numpy version:", np.__version__)

# Create sample DataFrame
data = {
    "Name": ["Amit", "Rahul", "John"],
    "Experience": [5, 4, 6],
    "Technology": ["Spark", "Python", "AWS"]
}

df = pd.DataFrame(data)

print("\nSample Data:")
print(df)

# Export to Excel
df.to_excel("test_output.xlsx", index=False)

print("\nExcel file created successfully!")
