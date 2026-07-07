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
print(df.columns)


# Category Revenue
category_revenue = df.groupby('Category')['Final Amount'].sum().reset_index()

# Payment Mode
payment_mode = df['Payment Mode'].value_counts()

# Monthly Trend
df['OrderDate'] = pd.to_datetime(df['OrderDate'])
df = df.sort_values('OrderDate')
monthly_date = df.groupby(df['OrderDate'].dt.to_period('M'))['Final Amount'].sum().reset_index()
monthly_date['OrderDate'] = monthly_date['OrderDate'].astype(str)

# Customer Revenue
customer_revn = df.groupby('CustomerID')['Final Amount'].sum().reset_index()

# Category wise Discount
category_discount = df.groupby('Category')['Discount'].sum().reset_index()




# 1. Bar Chart: Category Revenue
category = df['Category']
revenue = df['Final Amount']
plt.bar(category, revenue, label='Category', color='red', edgecolor='black')
plt.title('Category wise Analysis.')
plt.xlabel('Product Category.')
plt.ylabel('Revenue (INR)')
plt.legend()
plt.grid(True, axis='y', linestyle='--')
plt.savefig('visuals/01 Revenue by Category (BAR)')
plt.show()


# 2. Monthly Revenue Trend
plt.plot(monthly_date['OrderDate'], monthly_date['Final Amount'], label='Months', color='orange')
plt.title('Monthly Revenue Trend. (LINE)')
plt.xlabel('Months Name')
plt.ylabel('Revenue')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('visuals/02 Monthly Revenue Trend (Line).')
plt.show()


plt.pie(df['Category'], autopct='%1.1f%%', labels=df['Category'])
plt.title('Revenue Share by Category.(PIE)')
plt.legend()
plt.savefig('visuals/03 Revenue sahre by categpry.')
plt.show()




fig, axes = plt.subplots(nrows=2 , ncols=3, figsize=(10,8))


# 1. Bar chart: Category Revenue
axes[0,0].bar(category_revenue['Category'], category_revenue['Final Amount'], color='red', label='Category Revenue')
axes[0,0].set_title('Category Wise Revenue')
axes[0,0].set_xlabel('Category', fontsize=8)
axes[0,0].set_ylabel('Revenue')
axes[0,0].tick_params(axis='x', rotation=30  )

# 2. Pie Chart: Payment Mode
# axes[0,1].pie(payment_mode, autopct='%1.1f%%', startangle=90, labels=payment_mode.index)
# axes[0,1].set_title('Payment Mode')
category_sales = df.groupby('Category')['Amount_INR'].sum().reset_index()
axes[0,1].pie(category_sales['Amount_INR'], labels=category_sales['Category'], autopct= '%1.1f%%', startangle=90)
axes[0,1].set_title('Category Wise Revenue')

# 3. Line Char
# Monthly Sales Trend
axes[0,2].plot(monthly_date['OrderDate'], monthly_date['Final Amount'], marker='x', markersize=4, color='Blue' )
axes[0,2].set_title('Monthly Sales Trend')
axes[0,2].set_xlabel('Months')
axes[0,2].set_ylabel('Revenue')
axes[0,2].tick_params(axis='x', rotation=30)


# 4. Histogram
# Customer Revenue
axes[1,0].hist(df['CustomerID'].astype(str), bins=10, edgecolor='black')
axes[1,0].set_title('Customer Revenue')
axes[1,0].set_ylabel('Customer Count')
axes[1,0].set_xlabel('Customer ID')
axes[1,0].tick_params(axis='x', rotation=30, labelsize=8)


# 5. Scattor plot
# Category wise discount
axes[1,1].scatter(category_discount['Category'], category_discount['Discount'], color='orange')
axes[1,1].set_title('Category Wise Discount.')
axes[1,1].set_ylabel('Discount INR')
axes[1,1].set_xlabel('Category')
axes[1,1].tick_params(axis='x', rotation=30)


plt.tight_layout()
plt.show()