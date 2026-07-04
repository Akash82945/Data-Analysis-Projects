# import Library
import pandas as pd


# Load Dataset
df = pd.read_csv('data/Clean_sales.csv')
# print(df)
# print(df.columns)


# Total Revenue
revenue = df['Final Amount'].sum()

# Average Revenue
avg_rev = df['Final Amount'].mean()

# Highest Sale
highest_sale = df['Final Amount'].max()

# Lowest Sale
lowest_sale = df[df['Final Amount'] > 0]['Final Amount'].min()

# Category wise revenue
cat_revn = df.groupby('Category')['Final Amount'].sum().reset_index()

# Customer wise revenue
cust_revn = df.groupby('CustomerID')['Final Amount'].sum().reset_index()

# Monthly revenue
df['OrderDate'] = pd.to_datetime(df['OrderDate'])
df = df.sort_values('OrderDate')
monthly_date = df.groupby(df['OrderDate'].dt.to_period('M'))['Final Amount'].sum().reset_index()


# Top Customer
top_5_cust = cust_revn.sort_values(by='Final Amount', ascending=False)


# Top Categories
top_cat = cat_revn.sort_values(by='Final Amount', ascending=False)


print(f'''
===== Sales Analysis CLI =====\n
Total Revenue : {revenue}\n
Average Revenue : {avg_rev}\n
Highest Sale : {highest_sale}\n
Lowest Sale : {lowest_sale}\n
Category Wise Revenue :\n {cat_revn}\n
Customer Wise Revenue :\n {cust_revn}\n
Monthly Revenue :\n {monthly_date}\n
Top 5 Customer :\n {top_5_cust[:5]}\n
Top Categoey :\n {top_cat}\n
      ''')