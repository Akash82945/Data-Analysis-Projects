# import Library
import pandas as pd
from tabulate import tabulate

# Load Dataset
df = pd.read_csv('data/Clean_sales.csv')

# 1. KPI Calculations
revenue = df['Final Amount'].sum()
avg_rev = df['Final Amount'].mean()
highest_sale = df['Final Amount'].max()
lowest_sale = df[df['Final Amount'] > 0]['Final Amount'].min()

# 2. Category wise revenue
cat_revn_df = df.groupby('Category')['Final Amount'].sum().reset_index()
# टेबल के लिए tabulate फॉर्मेट में बदलें
cat_revn = tabulate(cat_revn_df, headers=["Category", "Revenue (₹)"], tablefmt="fancy_grid", showindex=False)

# 3. Top Categories
top_cat_df = cat_revn_df.sort_values(by='Final Amount', ascending=False)
top_cat = tabulate(top_cat_df, headers=["Category", "Revenue (₹)"], tablefmt="fancy_grid", showindex=False)

# 4. Customer wise revenue
cust_revn_df = df.groupby('CustomerID')['Final Amount'].sum().reset_index()
cust_revn = tabulate(cust_revn_df, headers=["Customer ID", "Revenue (₹)"], tablefmt="fancy_grid", showindex=False)

# 5. Top 5 Customer
top_5_cust_df = cust_revn_df.sort_values(by='Final Amount', ascending=False).head(5)
top_5_cust = tabulate(top_5_cust_df, headers=["Customer ID", "Total Spend (₹)"], tablefmt="fancy_grid", showindex=False)

# 6. Monthly revenue
df['OrderDate'] = pd.to_datetime(df['OrderDate'])
df = df.sort_values('OrderDate')
monthly_date_df = df.groupby(df['OrderDate'].dt.to_period('M'))['Final Amount'].sum().reset_index()
monthly_date_df['OrderDate'] = monthly_date_df['OrderDate'].astype(str) # पीरियड को स्ट्रिंग में बदलें
monthly_date = tabulate(monthly_date_df, headers=["Month", "Revenue (₹)"], tablefmt="fancy_grid", showindex=False)


# ====================================================
# OUTPUT PRINTING (YOUR EXACT CLI FORMAT WITH TABLES)
# ====================================================

print(f'''
===== Sales Analysis CLI =====

Total Revenue : ₹ {revenue:,.2f}

Average Revenue : ₹ {avg_rev:,.2f}

Highest Sale : ₹ {highest_sale:,.2f}

Lowest Sale : ₹ {lowest_sale:,.2f}

Category Wise Revenue :
{cat_revn}

Customer Wise Revenue :
{cust_revn}

Monthly Revenue :
{monthly_date}

Top 5 Customer :
{top_5_cust}

Top Category :
{top_cat}
''')
