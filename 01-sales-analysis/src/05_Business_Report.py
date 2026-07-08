import os
import pandas as pd
from tabulate import tabulate       # type:ignore

def generate_sales_report():
    author_name = "Akash"  
    
    csv_path = os.path.join("data", "Clean_sales.csv")
    report_path = os.path.join("reports", "Executive_Business_Report.md")
    
    if not os.path.exists(csv_path):
        csv_path = "01-sales-analysis/data/Clean_sales.csv"
        report_path = "01-sales-analysis/reports/Executive_Business_Report.md"

    df = pd.read_csv(csv_path)
    df['OrderDate'] = pd.to_datetime(df['OrderDate'])

    total_revenue = df['Final Amount'].sum()
    total_orders = len(df)
    avg_order_value = df['Final Amount'].mean()
    unique_customers = df['CustomerID'].nunique()
    highest_discount = df['Discount'].max()

    cat_perf = df.groupby('Category', as_index=False)['Final Amount'].sum()
    cat_perf_sorted = cat_perf.sort_values(by='Final Amount', ascending=False)
    highest_selling_cat = cat_perf_sorted.iloc[0]['Category']

    prod_quantity = df.groupby('Category', as_index=False)['Quantity'].sum()
    most_ordered_row = prod_quantity.sort_values(by='Quantity', ascending=False)
    most_ordered_product = most_ordered_row.iloc[0]['Category']
    most_ordered_qty = most_ordered_row.iloc[0]['Quantity']

    pay_perf = df.groupby('Payment Mode', as_index=False)['Final Amount'].sum()
    pay_perf = pay_perf.sort_values(by='Final Amount', ascending=False).copy()
    pay_perf['Final Amount'] = pay_perf['Final Amount'].apply(lambda x: f"₹{x:,.2f}")
    pay_table = tabulate(pay_perf.values, headers=["Payment Mode", "Total Revenue"], tablefmt="github")

    city_col = 'Location' if 'Location' in df.columns else ('City' if 'City' in df.columns else None)
    if city_col:
        city_perf = df.groupby(city_col, as_index=False)['Final Amount'].sum()
        city_perf = city_perf.sort_values(by='Final Amount', ascending=False).copy()
        city_perf['Final Amount'] = city_perf['Final Amount'].apply(lambda x: f"₹{x:,.2f}")
        city_table = tabulate(city_perf.values, headers=["City / Location", "Total Revenue"], tablefmt="github")
    else:
        city_table = "| City / Location | Total Revenue |\n| --- | --- |\n| N/A | Column not found in CSV |"

    cust_perf = df.groupby('CustomerID', as_index=False)['Final Amount'].sum()
    cust_perf_sorted = cust_perf.sort_values(by='Final Amount', ascending=False)
    top_customer = cust_perf_sorted.iloc[0]['CustomerID']
    top_customer_spend = cust_perf_sorted.iloc[0]['Final Amount']

    top_10_cust = cust_perf_sorted.head(10).copy()
    top_10_cust.insert(0, 'Rank', range(1, len(top_10_cust) + 1))
    top_10_cust['Final Amount'] = top_10_cust['Final Amount'].apply(lambda x: f"₹{x:,.2f}")
    top_10_cust_table = tabulate(top_10_cust.values, headers=["Rank", "Customer ID", "Total Spend"], tablefmt="github")

    top_10_prod = cat_perf_sorted.head(10).copy()
    top_10_prod.insert(0, 'Rank', range(1, len(top_10_prod) + 1))
    top_10_prod['Final Amount'] = top_10_prod['Final Amount'].apply(lambda x: f"₹{x:,.2f}")
    top_10_prod_table = tabulate(top_10_prod.values, headers=["Rank", "Category Name", "Total Revenue"], tablefmt="github")

    df = df.sort_values('OrderDate')
    monthly_perf = df.groupby(df['OrderDate'].dt.strftime('%B'), sort=False)['Final Amount'].sum().reset_index()
    monthly_perf.columns = ['Month', 'Total Revenue']
    monthly_perf['Growth_Pct'] = monthly_perf['Total Revenue'].pct_change() * 100
    monthly_perf['Month-over-Month Growth %'] = monthly_perf['Growth_Pct'].fillna(0).apply(
        lambda x: f"+{x:.2f}%" if x > 0 else (f"{x:.2f}%" if x < 0 else "Baseline")
    )
    monthly_perf['Total Revenue'] = monthly_perf['Total Revenue'].apply(lambda x: f"₹{x:,.2f}")
    monthly_perf_final = monthly_perf[['Month', 'Total Revenue', 'Month-over-Month Growth %']]
    monthly_table = tabulate(monthly_perf_final.values, headers=["Month", "Total Revenue", "Month-over-Month Growth %"], tablefmt="github")

    kpi_list = [
        ["Total Revenue", f"₹{total_revenue:,.2f}"],
        ["Total Orders", f"{total_orders:,} Orders"],
        ["Average Order Value (AOV)", f"₹{avg_order_value:,.2f}"],
        ["Unique Customers", f"{unique_customers:,}"],
        ["Highest Discount Given", f"₹{highest_discount:,.2f}"],
        ["Highest Selling Category", highest_selling_cat],
        ["Most Ordered Product (Qty)", f"{most_ordered_product} ({most_ordered_qty:,} Units)"],
        ["Top Customer", top_customer],
        ["Top Customer Revenue", f"₹{top_customer_spend:,.2f}"]
    ]
    kpi_table = tabulate(kpi_list, headers=["Metric", "Value"], tablefmt="github")

    insights_list1 = [
        ["Total Performance", f"The business generated total sales of **₹{total_revenue:,.2f}**."],
        ["Order Value", f"Average order value remained stable at **₹{avg_order_value:,.2f}** per transaction."],
        ["Customer Reach", f"Unique customer base stands at **{unique_customers:,}**, indicating a healthy market spread."]
    ]
    insights_table1 = tabulate(insights_list1, headers=["Aspect", "Finding"], tablefmt="github")

    insights_list2 = [
        ["Revenue Anchor", f"**{highest_selling_cat}**", "Highest overall financial revenue contributor."],
        ["Volume Anchor", f"**{most_ordered_product}**", f"Volume leader with **{most_ordered_qty:,}** total units sold."]
    ]
    insights_table2 = tabulate(insights_list2, headers=["Operational Metric", "Category Leader", "Data Insight"], tablefmt="github")

    insights_list3 = [
        ["Primary Top Client", f"**{top_customer}**", "Highest spending customer active during this period."],
        ["Core Focus Area", "Top 10 Accounts", "This specific group contributes a major portion of gross sales."]
    ]
    insights_table3 = tabulate(insights_list3, headers=["Customer segment", "Identifier", "Revenue contribution"], tablefmt="github")

    recommendations_list = [
        ["**Recommendation 1 – Inventory Optimization**", "High performance output from specific sectors.", f"Increase stock availability for **{highest_selling_cat}** to reduce missed sales opportunities."],
        ["**Recommendation 2 – Customer Retention**", "High enterprise value locked in single buyers.", f"Reward high-value customers like **{top_customer}** through loyalty programs, personalized offers, and exclusive membership benefits."],
        ["**Recommendation 3 – Marketing Strategy**", "Revenue flow fluctuates across operational periods.", "Run targeted promotional campaigns during slower months to improve sales consistency based on Monthly Growth trends."],
        ["**Recommendation 4 – Product Expansion**", "Market demand trends change over time.", "Expand the product catalog within high-performing categories based on customer demand trends."]
    ]
    recommendations_table = tabulate(recommendations_list, headers=["Focus Domain", "Identified Insight", "Mandatory Action Item"], tablefmt="github")

    takeaways_list = [
        ["Revenue Performance", "Strong overall financial revenue generation pipeline."],
        ["Segment Dependence", "Leading product category drives a large share of the business."],
        ["Client Concentration", "A small group of high-net-worth customers drives big volumes."],
        ["Planning Asset", "Monthly growth trend metrics can guide future seasonal planning."],
        ["Optimization Pivot", "Continuous data-driven analytics helps maximize profit and customer LTV."]
    ]
    takeaways_table = tabulate(takeaways_list, headers=["Strategic Area", "Core Summary Point"], tablefmt="github")

    report_content = f"""# 📊 Executive Business Report

**Project:** Sales Performance Analysis
**Generated By:** {author_name} (via Python Analytics Pipeline)
**Report Type:** Executive Summary
**Generated On:** *Automatically Generated by Python Script*

---

# 📌 Executive Summary

This report presents a high-level analysis of sales performance using cleaned transactional data. The objective is to identify key revenue drivers, customer purchasing behavior, category performance, and month-over-month business growth.

The analysis helps stakeholders make informed decisions related to inventory planning, customer retention, and sales strategy.

---

# 📈 Key Performance Indicators (KPIs)

{kpi_table}

---

# 📅 Monthly Revenue & Growth Performance

{monthly_table}

---

# 💳 Revenue by Payment Mode

{pay_table}

---

# 🏙️ Revenue by City / Location

{city_table}

---

# 🏆 Top 10 Customers by Revenue

{top_10_cust_table}

---

# 📦 Top 10 Product Categories by Revenue

{top_10_prod_table}

---

# 📊 Business Insights

## 1. Revenue Overview

{insights_table1}

## 2. Category Performance

{insights_table2}

## 3. Customer Analysis

{insights_table3}

---

# 💡 Strategic Business Recommendations

{recommendations_table}

---

# 📌 Key Takeaways

{takeaways_table}

---

# 📁 Report Information

| Item                | Description             |
| ------------------- | ----------------------- |
| Dataset             | Clean_sales.csv         |
| Language            | Python                  |
| Libraries           | Pandas, Tabulate        |
| Output Format       | Markdown (.md)          |
| Report Generated By | Automated Python Script |

---

**End of Report**"""

    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
    
    print(f"\n📄 [SUCCESS] Report generated successfully using Tabulate: {report_path}")

if __name__ == "__main__":
    generate_sales_report()
