# import Library
import pandas as pd
from tabulate import tabulate   #type:ignore  # टेबल फॉर्मेट के लिए लाइब्रेरी


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
cat_tab = tabulate(cat_revn, headers=['Category', 'Revenue(₹)'], tablefmt='fancy_grid', showindex=False)

# Customer wise revenue
cust_revn = df.groupby('CustomerID')['Final Amount'].sum().reset_index()
cust_revn_tab = tabulate(cust_revn, headers=['Customer ID','Revenue(₹)'],tablefmt='fancy_grid',showindex=False)


# Monthly revenue
df['OrderDate'] = pd.to_datetime(df['OrderDate'])
df = df.sort_values('OrderDate')
monthly_date = df.groupby(df['OrderDate'].dt.to_period('M'))['Final Amount'].sum().reset_index()
monthly_date['OrderDate'] = monthly_date['OrderDate'].astype(str)
month_tab = tabulate(monthly_date, headers=['Month','Revenue(₹)'],tablefmt='fancy_grid',showindex=False)

# Top Customer
top_5_cust = cust_revn.sort_values(by='Final Amount', ascending=False).head(5)
top_cust = tabulate(top_5_cust, headers=['Customer ID','Total Spend(₹)'],tablefmt='fancy_grid',showindex=False)


# Top Categories
top_cat = cat_revn.sort_values(by='Final Amount', ascending=False)
top_cat_tab = tabulate(top_cat, headers=['Categories','Revenue(₹)'],tablefmt='fancy_grid',showindex=False)



# print(f'''
# ===== Sales Analysis CLI =====\n
# Total Revenue : {revenue}\n
# Average Revenue : {avg_rev}\n
# Highest Sale : {highest_sale}\n
# Lowest Sale : {lowest_sale}\n
# Category Wise Revenue :\n {cat_revn}\n
# Customer Wise Revenue :\n {cust_revn}\n
# Monthly Revenue :\n {monthly_date}\n
# Top 5 Customer :\n {top_5_cust[:5]}\n
# Top Categoey :\n {top_cat}\n
#       ''')



print("\n" + "="*50)
print("             SALES ANALYSIS DASHBOARD             ")
print("="*50)

kpi_data = [
    ["Total Revenue", f"₹ {revenue:,.2f}"],
    ["Average Revenue", f"₹ {avg_rev:,.2f}"],
    ["Highest Sale", f"₹ {highest_sale:,.2f}"],
    ["Lowest Sale", f"₹ {lowest_sale:,.2f}"]
]
print("\n[ REVENUE MATRICS ]")
print(tabulate(kpi_data, headers=["Columns", "Value"], tablefmt="fancy_grid"))

print(f'''
Category Wise Revenue:\n{cat_tab}\n
Customer Wise Revenue:\n{cust_revn_tab}\n
Monthly Revenue:\n{month_tab}\n
Top 5 Customer:\n{top_cust}\n
Top Categoey:\n{top_cat_tab}\n
      ''')