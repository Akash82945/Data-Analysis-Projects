# import Library
import os
import pandas as pd
from tabulate import tabulate  # type:ignore

def generate_sales_report():
    # Setup paths according to your folder structure
    csv_path = os.path.join("01-sales-analysis", "data", "Clean_sales.csv")
    report_path = os.path.join("01-sales-analysis", "reports", "Executive_Business_Report.md")
    
    # Backup paths if executed directly from src folder
    if not os.path.exists(csv_path):
        csv_path = "data/Clean_sales.csv"
        report_path = "reports/Executive_Business_Report.md"

    # Load dataset
    df = pd.read_csv(csv_path)
    df['OrderDate'] = pd.to_datetime(df['OrderDate'])

    # ====================================================
    # BUSINESS LOGIC & CALCULATIONS
    # ====================================================
    
    # 1. Core Revenue Metrics
    total_revenue = df['Final Amount'].sum()
    avg_revenue = df['Final Amount'].mean()

    # 2. Highest Selling Category
    cat_perf = df.groupby('Category')['Final Amount'].sum().reset_index()
    top_cat_row = cat_perf.sort_values(by='Final Amount', ascending=False).iloc[0]
    highest_selling_cat = top_cat_row['Category']
    highest_cat_rev = top_cat_row['Final Amount']

    # 3. Top Customer
    cust_perf = df.groupby('CustomerID')['Final Amount'].sum().reset_index()
    top_cust_row = cust_perf.sort_values(by='Final Amount', ascending=False).iloc[0]
    top_customer = top_cust_row['CustomerID']
    top_customer_spend = top_cust_row['Final Amount']

    # 4. Monthly Growth Analysis
    df = df.sort_values('OrderDate')
    monthly_perf = df.groupby(df['OrderDate'].dt.to_period('M'))['Final Amount'].sum().reset_index()
    monthly_perf['OrderDate'] = monthly_perf['OrderDate'].astype(str)
    
    # Calculate Month-over-Month Growth Percentage
    monthly_perf['Growth (%)'] = monthly_perf['Final Amount'].pct_change() * 100
    monthly_perf['Growth (%)'] = monthly_perf['Growth (%)'].fillna(0).apply(
        lambda x: f"{x:+.2f}%" if x != 0 else "Baseline"
    )

    # ====================================================
    # TABLES PREPARATION FOR TERMINAL & FILE
    # ====================================================
    
    # Prepare executive summary rows
    kpi_data = [
        ["Total Revenue", f"INR {total_revenue:,.2f}"],
        ["Average Revenue", f"INR {avg_revenue:,.2f}"],
        ["Highest Selling Category", f"{highest_selling_cat} (INR {highest_cat_rev:,.2f})"],
        ["Top Customer", f"{top_customer} (INR {top_customer_spend:,.2f})"]
    ]
    
    # Format monthly data frame for clean grid printing
    monthly_formatted = monthly_perf.copy()
    monthly_formatted['Final Amount'] = monthly_formatted['Final Amount'].apply(lambda x: f"INR {x:,.2f}")

    # ====================================================
    # 1. PRINT TO TERMINAL (CLI OUTPUT)
    # ====================================================
    print("\n" + "="*60)
    print("                      ========== SALES REPORT ==========                      ")
    print("="*60)
    
    print("\n[ EXECUTIVE SUMMARY ]")
    print(tabulate(kpi_data, headers=["Metric", "Insight Value"], tablefmt="fancy_grid"))

    print("\n[ MONTHLY PERFORMANCE & GROWTH ]")
    print(tabulate(monthly_formatted, headers=["Month", "Total Revenue", "MoM Growth"], tablefmt="fancy_grid", showindex=False))

    print("\n[ BUSINESS RECOMMENDATIONS ]")
    rec1 = f"1. 🔥 Double Down on {highest_selling_cat}: This category drives your highest value. Maintain optimum inventory and introduce premium variants."
    rec2 = f"2. 💎 VIP Loyalty Program: Customer {top_customer} is your most valuable buyer. Launch exclusive retention campaigns or rewards for them."
    rec3 = f"3. 📈 Seasonality Strategy: Use targeted marketing or flash sales during months showing flat or negative MoM trends to stabilize revenue flow."
    
    print(rec1)
    print(rec2)
    print(rec3)
    print("\n" + "="*60)

    # ====================================================
    # 2. SAVE TO EXPORT FILE (.MD)
    # ====================================================
    report_content = f"""# Executive Business Report
**Generated Automatically from Clean Data** | Date: 2026

## 📊 Executive Summary (Key Metrics)
Below are the high-level business performance metrics:

{tabulate(kpi_data, headers=["Metric", "Insight Value"], tablefmt="github")}

## 📈 Monthly Revenue & Growth Trend
Track breakdown of total revenue generation alongside month-over-month shifts:

{tabulate(monthly_formatted, headers=["Month", "Total Revenue", "MoM Growth"], tablefmt="github", showindex=False)}

## 💡 Business Recommendations
* **Category Focus**: {rec1[3:]}
* **Customer Value**: {rec2[3:]}
* **Growth Vectors**: {rec3[3:]}
"""
    
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"\n📄 Report successfully exported to Markdown file: {report_path}")

if __name__ == "__main__":
    generate_sales_report()
