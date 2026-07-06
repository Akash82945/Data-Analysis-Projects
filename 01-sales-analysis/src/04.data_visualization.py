import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("data/Clean_sales.csv")
# print(df.columns)


total_sales = df['Final Amount'].sum()
average_sales = df['Final Amount'].mean()
highest_sales = df['Final Amount'].max()
lowest_sales = df['Final Amount'].min()

df['OrderDate'] = pd.to_datetime(df['OrderDate'])
df['OrderDate'] = df.sort_values('OrderDate')
monthly_date = df.groupby(df['OrderDate'].dt.to_period('M'))['Final Amount'].sum().reset_index()
monthly_date['OrderDate'] = monthly_date['OrderDate'].astype(str)

cust_revn = df.groupby('CustomerID')['Final Amount'].sum().reset_index()

cat_revn = df.groupby('Category')['Final Amount'].sum().reset_index()

top_cust = df.groupby('CustomerID')['Final Amount'].sum().reset_index().head(5)

fig, axes = plt.subplot(3,1, figsize=(10,8))
fig.subplot("Sales Performance Analysis Dashboard.", fontsize=14, fontweight='bold', y=0.98)

sns.lineplot(ax=axes[0], data=monthly_date, x='OrderDate', y='Final Amount')
axes[0].set_title('Monthly Revenue Trend', fontsize=10, fontweight='bold')
axes[0].set_xlabel('Months')
axes[0].set_ylabel('Revenue')
axes[0].tick_params(axis='x', rotation=45)
axes[0].set_tight_layout()


sns.barplot(ax=axes[1], data='Category Revenue', x='Categoey', y='Final Amount')
axes[1].set_title('Category wise Revenue (BAR CHART)')
axes[1].set_xlabel('Categories')
axes[1].set_ylabel('Revenues')
axes[1].tick_params(rotation=40)
axes[1].set_tight_layout()


sns.histplot(ax=[2], data=cust_revn, x='CustomerID', y='Final Amount')
ax[2].set_title("Customer wise Revenue")
ax[2]
ax[2]
ax[2]
ax[2]
ax[2]