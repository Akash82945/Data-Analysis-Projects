# # import Library
# import pandas as pd
# from tabulate import tabulate   #type:ignore  # टेबल फॉर्मेट के लिए लाइब्रेरी


# # Load Dataset
# df = pd.read_csv('data/Clean_sales.csv')
# # print(df)
# # print(df.columns)


# # Total Revenue
# revenue = df['Final Amount'].sum()

# # Average Revenue
# avg_rev = df['Final Amount'].mean()

# # Highest Sale
# highest_sale = df['Final Amount'].max()

# # Lowest Sale
# lowest_sale = df[df['Final Amount'] > 0]['Final Amount'].min()

# # Category wise revenue
# cat_revn = df.groupby('Category')['Final Amount'].sum().reset_index()
# cat_tab = tabulate(cat_revn, headers=['Category', 'Revenue(₹)'], tablefmt='fancy_grid', showindex=False)

# # Customer wise revenue
# cust_revn = df.groupby('CustomerID')['Final Amount'].sum().reset_index()
# cust_revn_tab = tabulate(cust_revn, headers=['Customer ID','Revenue(₹)'],tablefmt='fancy_grid',showindex=False)


# # Monthly revenue
# df['OrderDate'] = pd.to_datetime(df['OrderDate'])
# df = df.sort_values('OrderDate')
# monthly_date = df.groupby(df['OrderDate'].dt.to_period('M'))['Final Amount'].sum().reset_index()
# monthly_date['OrderDate'] = monthly_date['OrderDate'].astype(str)
# month_tab = tabulate(monthly_date, headers=['Month','Revenue(₹)'],tablefmt='fancy_grid',showindex=False)

# # Top Customer
# top_5_cust = cust_revn.sort_values(by='Final Amount', ascending=False).head(5)
# top_cust = tabulate(top_5_cust, headers=['Customer ID','Total Spend(₹)'],tablefmt='fancy_grid',showindex=False)


# # Top Categories
# top_cat = cat_revn.sort_values(by='Final Amount', ascending=False)
# top_cat_tab = tabulate(top_cat, headers=['Categories','Revenue(₹)'],tablefmt='fancy_grid',showindex=False)




# print("\n" + "="*50)
# print("             SALES ANALYSIS DASHBOARD             ")
# print("="*50)

# kpi_data = [
#     ["Total Revenue", f"₹ {revenue:,.2f}"],
#     ["Average Revenue", f"₹ {avg_rev:,.2f}"],
#     ["Highest Sale", f"₹ {highest_sale:,.2f}"],
#     ["Lowest Sale", f"₹ {lowest_sale:,.2f}"]
# ]
# print("\n[ REVENUE MATRICS ]")
# print(tabulate(kpi_data, headers=["Columns", "Value"], tablefmt="fancy_grid"))

# print(f'''
# Category Wise Revenue:\n{cat_tab}\n
# Customer Wise Revenue:\n{cust_revn_tab}\n
# Monthly Revenue:\n{month_tab}\n
# Top 5 Customer:\n{top_cust}\n
# Top Categoey:\n{top_cat_tab}\n
#       ''')





import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Folders setup karna taaki error na aaye
os.makedirs('visuals', exist_ok=True)

# 2. Cleaned Data Load karna
# Agar aapka data path thoda alag hai toh yahan badal sakte hain
try:
    df = pd.read_csv('data/Clean_sales.csv')
    df['OrderDate'] = pd.to_datetime(df['OrderDate'])
except FileNotFoundError:
    print("Error: 'data/Clean_sales.csv' nahi mili! Pehle cleaning script run karein.")
    exit()
    
# 1. Data load hone ke baad columns check karne ke liye
df = pd.read_csv('data/Clean_sales.csv')

print("\n🔍 AAPKE DATA MEIN YEH COLUMNS HAIN:")
print(list(df.columns))  # Yeh terminal par saare exact naam print kar dega
print("-" * 40)

# 2. Automatically kisi bhi product-related column ko dhoondhne ke liye (Safe Approach)
# Yeh check karega ki kis column ke naam mein 'product' word aa raha hai
product_col = [col for col in df.columns if 'product' in col.lower()]

if product_col:
    actual_product_column = product_col[0]
    print(f"✅ Auto-Detected Product Column: '{actual_product_column}'\n")
else:
    print("❌ Error: Koi bhi product-related column nahi mila!")
    actual_product_column = None

# Style setting for professional look
plt.style.use('ggplot')
colors_palette = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

print("📈 Graphs generate ho rahe hain, kripya thoda intezar karein...")

# --- CHART 1: Revenue by Category (Bar Chart) ---
plt.figure(figsize=(10, 6))
category_revenue = df.groupby('Category')['Final Amount'].sum().sort_values(ascending=False)
category_revenue.plot(kind='bar', color=colors_palette[:len(category_revenue)], edgecolor='black')
plt.title('Total Revenue by Product Category', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Category', fontsize=12)
plt.ylabel('Revenue ($)', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('visuals/01_Revenue_by_Category.png', dpi=300)
plt.close()

# --- CHART 2: Monthly Revenue Trend (Line Chart) ---
plt.figure(figsize=(12, 6))
df['Month'] = df['OrderDate'].dt.to_period('M')
monthly_revenue = df.groupby('Month')['Final Amount'].sum()
monthly_revenue.index = monthly_revenue.index.to_timestamp() # String se datetime mein convert for plotting

plt.plot(monthly_revenue.index, monthly_revenue.values, marker='o', linestyle='-', color='#d62728', linewidth=2.5)
plt.title('Monthly Revenue Trend Growth', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Months', fontsize=12)
plt.ylabel('Revenue ($)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('visuals/02_Monthly_Revenue_Trend.png', dpi=300)
plt.close()

# --- CHART 3: Revenue Share by Category (Pie Chart) ---
plt.figure(figsize=(8, 8))
plt.pie(category_revenue, labels=category_revenue.index, autopct='%1.1f%%', 
        startangle=140, colors=colors_palette, wedgeprops={'edgecolor': 'white', 'linewidth': 1})
plt.title('Percentage Revenue Share by Category', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('visuals/03_Revenue_Share.png', dpi=300)
plt.close()

# --- CHART 4: Top Customers (Horizontal Bar Chart) ---
plt.figure(figsize=(10, 6))
top_customers = df.groupby('CustomerID')['Final Amount'].sum().sort_values(ascending=False).head(10)
top_customers.plot(kind='barh', color='#2ca02c', edgecolor='black').invert_yaxis() # Top customer sabse upar dikhane ke liye
plt.title('Top 10 Customers by Revenue Contribution', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Total Spent ($)', fontsize=12)
plt.ylabel('Customer ID', fontsize=12)
plt.tight_layout()
plt.savefig('visuals/04_Top_Customers.png', dpi=300)
plt.close()

# --- CHART 5: Top Products (Bar Chart) ---
plt.figure(figsize=(12, 6))
top_products = df.groupby('Product Name')['Final Amount'].sum().sort_values(ascending=False).head(10)
top_products.plot(kind='bar', color='#ff7f0e', edgecolor='black')
plt.title('Top 10 Best Selling Products', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Product Name', fontsize=12)
plt.ylabel('Revenue ($)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('visuals/05_Top_Products.png', dpi=300)
plt.close()

# --- BONUS CHART 6: Master Dashboard (Sabhi Ka Combo) ---
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('🚀 Sales Executive Analytics Dashboard', fontsize=20, fontweight='bold', y=0.98)

# Top Left: Revenue by Category
category_revenue.plot(kind='bar', ax=axes[0,0], color=colors_palette, edgecolor='black')
axes[0,0].set_title('Revenue by Category')
axes[0,0].tick_params(axis='x', rotation=30)

# Top Right: Monthly Trend
axes[0,1].plot(monthly_revenue.index, monthly_revenue.values, marker='o', color='#d62728')
axes[0,1].set_title('Monthly Sales Trend')
axes[0,1].grid(True, alpha=0.4)

# Bottom Left: Revenue Share
axes[1,0].pie(category_revenue, labels=category_revenue.index, autopct='%1.1f%%', colors=colors_palette, startangle=90)
axes[1,0].set_title('Revenue % Share')

# Bottom Right: Top Customers
top_customers.head(5).plot(kind='barh', ax=axes[1,1], color='#2ca02c', edgecolor='black').invert_yaxis()
axes[1,1].set_title('Top 5 Customers')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('visuals/Dashboard.png', dpi=300)
plt.close()

print("✅ Saare visuals aur 'Dashboard.png' successfully 'visuals/' folder mein save ho gaye hain!")