import pandas as pd
import matplotlib.pyplot as plt
from pyparsing import Char


df = pd.read_csv('data/Clean_sales.csv')
print(df.columns)


# Category Revenue(for 1 Chart)
category_revenue = df.groupby('Category')['Final Amount'].sum().reset_index()


# Monthly Trend
df['OrderDate'] = pd.to_datetime(df['OrderDate'])
df = df.sort_values('OrderDate')
monthly_date = df.groupby(df['OrderDate'].dt.to_period('M'))['Final Amount'].sum().reset_index()
monthly_date['OrderDate'] = monthly_date['OrderDate'].astype(str)




# 1. Bar Chart: Category Revenue
cat_revn = df.groupby('Category')['Final Amount'].sum().reset_index()
plt.bar(
    cat_revn['Category'], 
    cat_revn['Final Amount'], 
    label='Category', 
    color='red', 
    edgecolor='black'
)
plt.title('Category wise Analysis.')
plt.xlabel('Product Category.')
plt.ylabel('Revenue (INR)')
plt.legend()
plt.grid(True, axis='y', linestyle='--')
plt.savefig('visuals/01_Revenue_by_Category_Bar')
plt.show()


# 2. Monthly Revenue Trend
plt.plot(
    monthly_date['OrderDate'], 
    monthly_date['Final Amount'], 
    label='Months', 
    color='orange', 
    marker='o', 
    markersize=8
)
plt.title('Monthly Revenue Trend. (LINE)')
plt.xlabel('Months Name')
plt.ylabel('Revenue')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('visuals/02_Monthly_Revenue_Trend_Line.')
plt.show()


# 3. Revenue share by category 
plt.pie(
    category_revenue['Final Amount'], 
    autopct='%1.1f%%', 
    labels=category_revenue['Category'],
    startangle=90
)
plt.title('Revenue Share by Category.(PIE)')
plt.legend()
plt.xticks(rotation=40, ha='right')
plt.tight_layout()
plt.savefig('visuals/03_Revenue_Sahre_by_Categpry.')
plt.show()


# 4. Top 5 Customer by Revenue(Bar);
plt.figure(figsize=(8, 5))
customer_revn = df.groupby('CustomerID')['Final Amount'].sum().reset_index().sort_values(by='Final Amount', ascending=False).head(5)
plt.bar(
    customer_revn['CustomerID'], 
    customer_revn['Final Amount'], 
    color='orange', 
    edgecolor='black'
)
plt.title("Top 5 Customer.")
plt.xlabel('Revenue')
plt.ylabel('Revenue ID')
plt.tight_layout()
plt.grid(True)
plt.xticks(rotation=30)
plt.savefig('visuals/04_Top_5_Customer')
plt.show()
plt.close() 



# 5. Quantity Sold by Category (BAR)
plt.figure(figsize=(8, 5))
quantity_sold = df.groupby('Category')['Quantity'].sum().reset_index()
plt.bar(
    quantity_sold['Category'], 
    quantity_sold['Quantity'], 
    label='Category', 
    color='pink', 
    edgecolor='black'
)
plt.title('Quantity Sold by Category. (BAR)')
plt.xlabel('Category')
plt.ylabel('Quantity')
plt.grid(True, axis='y', linestyle='--')
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig('visuals/05_Quantity_sold_by_Category.')
plt.show()
plt.close() 



# 06. Order Amount Distribution
fig, (ax_box, ax_hist) = plt.subplots(2, sharex=True, gridspec_kw={'height_ratios':(.15,.85)}, figsize=(8,6))
ax_box.boxplot(df['Final Amount'], vert=False)
ax_box.set_title('Order Amount Distribution Analysis')
ax_box.axis('off')

ax_hist.hist(
    df['Final Amount'], 
    bins=20, 
    color='skyblue', 
    edgecolor='black'
)
ax_hist.set_xlabel('Order Amount (INR)')
ax_hist.set_ylabel('Number of orders')
ax_hist.grid(True)
plt.tight_layout()
plt.savefig('visuals/06_Order_Amount_Distribution')
plt.show()





fig, axes = plt.subplots(nrows=2 , ncols=3, figsize=(13,10))


# 1. Bar chart: Category Revenue
axes[0,0].bar(
    category_revenue['Category'], 
    category_revenue['Final Amount'], 
    color='red', label='Category Revenue',  
    edgecolor='black'
)
axes[0,0].set_title('Category Wise Revenue')
axes[0,0].set_xlabel('Category', fontsize=8)
axes[0,0].set_ylabel('Revenue')
axes[0,0].tick_params(axis='x', rotation=30  )

# 2. Pie Chart: Category wise Revenue
category_sales = df.groupby('Category')['Amount_INR'].sum().reset_index()
axes[0,1].pie(
    category_sales['Amount_INR'], 
    labels=category_sales['Category'], 
    autopct= '%1.1f%%', 
    startangle=90
)
axes[0,1].set_title('Category Wise Revenue')

# 3. Line Char: Monthly Sales Trend
axes[0,2].plot(
    monthly_date['OrderDate'], 
    monthly_date['Final Amount'], 
    marker='o', 
    markersize=6, 
    color='Blue' 
)
axes[0,2].set_title('Monthly Sales Trend')
axes[0,2].set_xlabel('Months')
axes[0,2].set_ylabel('Revenue')
axes[0,2].tick_params(axis='x', rotation=30)


# 4. Histogram: Customer Revenue
axes[1,0].hist(
    df['CustomerID'].astype(str), 
    bins=10,
    edgecolor='black'
)
axes[1,0].set_title('Customer Revenue')
axes[1,0].set_ylabel('Customer Count')
axes[1,0].set_xlabel('Customer ID')
axes[1,0].tick_params(axis='x', rotation=30, labelsize=8)


# 5. Scattor plot: Category wise discount
category_discount = df.groupby('Category')['Discount'].sum().reset_index()
axes[1,1].scatter(
    category_discount['Category'], 
    category_discount['Discount'], 
    color='orange',
    marker='o',
    s =40,
    edgecolor='black'    
)
axes[1,1].set_title('Category Wise Discount.')
axes[1,1].set_ylabel('Discount INR')
axes[1,1].set_xlabel('Category')
axes[1,1].tick_params(axis='x', rotation=30)


ax_qa = axes[1,2]
ax_qa.axis('off')

top_cat = category_revenue.sort_values(by='Final Amount', ascending=False)
top_cust = customer_revn.iloc[0]['CustomerID']
total_sales = df['Final Amount'].sum()

qa_text = (
    'BUSINESS INSIGHTS & Q&A\n'
    '--------------------------\n\n'
    'Q1: Which category drives the most revenue?\n'
    f'Ans: {top_cat} is our top performer.\n\n'
    
     "Q2: Who is our most valuable customer?\n"
    f"Ans: {top_cust} generated the highest sales.\n\n"
    
    "Q3: What is the total business revenue?\n"
    f"Ans: INR {total_sales:,.2f}\n\n"
    
    "Recommendation:\n"
    f"Focus marketing budgets on {top_cat}\n"
    "and give loyalty rewards to top clients."
)

ax_qa.text(0.01, 0.95, qa_text, fontsize=9.5, verticalalignment='top', 
           fontfamily='sans-serif', color='#1a1a1a',
           bbox=dict(boxstyle='round,pad=1', facecolor='#f4f6f9', edgecolor='#ccc'))




plt.tight_layout(pad=3.0)
fig.subplots_adjust(bottom=0.12)

plt.savefig('visuals/DashBoard_Chart')
plt.show()