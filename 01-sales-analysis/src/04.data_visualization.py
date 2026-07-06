# import pandas as pd 
# import matplotlib.pyplot as plt
# import seaborn as sns

# df = pd.read_csv("data/Clean_sales.csv")
# # print(df.columns)


# total_sales = df['Final Amount'].sum()
# average_sales = df['Final Amount'].mean()
# highest_sales = df['Final Amount'].max()
# lowest_sales = df['Final Amount'].min()

# df['OrderDate'] = pd.to_datetime(df['OrderDate'])
# df = df.sort_values('OrderDate')
# monthly_date = df.groupby(df['OrderDate'].dt.to_period('M'))['Final Amount'].sum().reset_index()
# monthly_date['OrderDate'] = monthly_date['OrderDate'].astype(str)

# cust_revn = df.groupby('CustomerID')['Final Amount'].sum().reset_index()

# cat_revn = df.groupby('Category')['Final Amount'].sum().reset_index()

# top_cust = df.groupby('CustomerID')['Final Amount'].sum().reset_index()

# fig, axes = plt.subplots(3,1, figsize=(10,8))
# fig.suptitle("Sales Performance Analysis Dashboard.", fontsize=14, fontweight='bold', y=0.98)

# sns.lineplot(ax=axes[0], data=monthly_date, x='OrderDate', y='Final Amount')
# axes[0].set_title('Monthly Revenue Trend', fontsize=10, fontweight='bold')
# axes[0].set_xlabel('Months')
# axes[0].set_ylabel('Revenue')
# axes[0].tick_params(axis='x', rotation=45)


# sns.barplot(ax=axes[1], data=cat_revn, x='Category', y='Final Amount', palette='viridis')
# axes[1].set_title('Category wise Revenue (BAR CHART)')
# axes[1].set_xlabel('Categories')
# axes[1].set_ylabel('Revenues')
# axes[1].tick_params(rotation=40)


# sns.histplot(ax=axes[2], data=cust_revn, x='CustomerID', y='Final Amount')
# axes[2].set_title("Customer wise Revenue")
# axes[2].set_xlabel('Customer')
# axes[2].set_ylabel('Revenue')
# axes[2].tick_params(rotation=40)

# plt.tight_layout()
# plt.show()




import pandas as pd
import matplotlib.pyplot as plt
from pyparsing import Char


df = pd.read_csv('data/Clean_sales.csv')
print(df.cloumn)


category_revenue = df.groupby('Category')['Final Amount'].sum().reset_index()
payment_mode = df['Payment Mode'].value_counts()
df['OrderDate'] = pd.to_datetime(df['OrderDate'])
df = df.sort_values('OrderDate')
monthly_date = df.groupby('Months')['Final Amount'].sum().reindex(['January', 'Februaru', 'March'])
customer_revn = df.groupby('CustomerID')['Final Amount'].sum().reset_index()
category_discount = df.groupby('Catogary')['Discount'].sum().reset_index()


fig, axes = plt.subplots(nrows=2 , ncols=2, figsize=(10,8))


# 1. Bar chart
# Category Revenue
axes[0,0].bar(category_revenue, color='red', label='Category Revenue')
axes[0,0].set_title('Category Wise Revenue')
axes[0,0].set_xlabel('Category')
axes[0,0].set_ylabel('Revenue')
axes[0,0]

# 2. Pie Chart
# Paymrnt Mode



# 3. Line Char
# Monthly Sales Trend



# 4. Histogram
# Customer Revenue




# 5. Scattor plot
# Category wise discout
