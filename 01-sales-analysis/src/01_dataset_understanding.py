# Libraries
import pandas as pd
import matplotlib.pyplot as plt

# Load Dataset
df = pd.read_csv('data/Sales.csv')


# Print top 5 Rows/ Quick Review of Dataset
print('Head of dataset\n',df.head())
print('\n')

# Print bottom 5 Rows
print('Tail of dataset\n',df.tail())
print('\n')


# Print Shape of dataset
print('Shape of dataset\n',df.shape)
print('\n')

# Print Columns of Dataset
print('Columns of dataset\n',df.columns)
print('\n')


# Print Data Types 
print('Data type of data\n',df.dtypes)
print('\n')

# Print data Information
print('Information of data')
information = df.info()
print(information)
print('\n')


# Describe the Dataset
print('Mathematical summary')
describe = df.describe()
print(describe)
print('\n')


# Missing Values
print("Missing Values")
missing_values = df.isnull().sum()
row_value = df[df.isnull().any(axis=1)]
print(missing_values)
print('List of Missing Values :-\n',row_value)
print('\n')


# Dupplicate Values
print('Duplicate Values')
duplicate = df.duplicated().sum()
print(duplicate)
print('\n')

# Number of unique custumnes
print('Unique Customers')
unique_cust = df['CustomerID'].unique()
count_unique = df['CustomerID'].nunique()
print(unique_cust)
print('No of unique Customer:- ',count_unique)
print('\n')


# Number of Categories
print('Number of Categories.')
category = df['Category'].unique()
print(category)