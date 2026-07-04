# import Library
import pandas as pd


# Load Dataset
df = pd.read_csv('data/Sales.csv')
print(df.head())


# Save csv file path
csv_path = 'data/Clean_sales.csv'


# Check missing values
missing_val = df.isnull().sum()
print(missing_val)


# Handle Missing Values
handle_missing_val = df.fillna(0)
print('Successfully Handle Missing Values.')


# Check any duplicate Values
duplicate = df.duplicated().sum()
print(f'Duplicate Values in Dataset :- {duplicate}')

if duplicate > 0:
    df_cleaned = df.drop_duplicates(keep='first')
    
    df_cleaned.to_csv(csv_path, index=False)
    print('Duplicate Removed Successfully.')
else:
    print("None Duplicate Data find in dataset")
    

# Convert OrderDate column into datetime column
df['OrderDate'] = pd.to_datetime(df['OrderDate'], errors='coerce')

numeric_col = ['Salary', 'Quantity', 'Amount_INR', 'Discount', 'Final Amount']
for col in numeric_col:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    

# Save Cleaned Dataset
df.to_csv(csv_path, index=False)
print('Data Saved Successfully')