import pandas as pd
import sqlite3
import os

print("=== SPRINT 3: RELATIONAL DATABASE & SQL ANALYTICS ===\n")

# -------------------------------------------------------------
# TASK 1: Create SQLite Database and Ingest Tables
# -------------------------------------------------------------
db_name = 'diwali_economy.db'
conn = sqlite3.connect(db_name)
print(f"Connected to SQLite Database: {db_name}")

try:
    # 1. Load and ingest Kaggle Sales Data into SQLite
    if os.path.exists('Diwali Sales Data.csv'):
        df_sales = pd.read_csv('Diwali Sales Data.csv', encoding='latin1')
    else:
        df_sales = pd.read_excel('Diwali Sales Data.xlsx')
        
    df_sales = df_sales.drop_duplicates()
    df_sales['Amount'] = df_sales['Amount'].fillna(df_sales.groupby('Product_Category')['Amount'].transform('median'))
    
    # Write to SQL table
    df_sales.to_sql('fact_transactions', conn, if_exists='replace', index=False)
    print("-> Table 'fact_transactions' created successfully.")

    # 2. Load and ingest VAHAN Monthly Data into SQLite
    def load_vahan(filename_base):
        if os.path.exists(filename_base + '.csv'):
            return pd.read_csv(filename_base + '.csv')
        else:
            return pd.read_excel(filename_base + '.xlsx')

    df_m1 = load_vahan('2020-2022 montwise vahan').iloc[:, :2]
    df_m2 = load_vahan('2023-2025 montiwse vahan').iloc[:, :2]
    df_m1.columns = ['Month', 'Total_Registrations']
    df_m2.columns = ['Month', 'Total_Registrations']
    
    df_vahan = pd.concat([df_m1, df_m2], ignore_index=True)
    df_vahan['Month_Str'] = df_vahan['Month'].astype(str).str.strip()
    df_vahan = df_vahan[df_vahan['Month_Str'].str.match(r'^\d{4}-\d{2}$')]
    df_vahan['Month_DT'] = pd.to_datetime(df_vahan['Month_Str'], format='%Y-%m')
    df_vahan['Year'] = df_vahan['Month_DT'].dt.year
    df_vahan['Month_Num'] = df_vahan['Month_DT'].dt.month
    df_vahan['Total_Registrations'] = pd.to_numeric(df_vahan['Total_Registrations'], errors='coerce')
    df_vahan['Is_Festival_Month'] = df_vahan['Month_Num'].isin([10, 11]).astype(int)
    
    # Write to SQL table
    df_vahan.to_sql('fact_vehicle_registrations', conn, if_exists='replace', index=False)
    print("-> Table 'fact_vehicle_registrations' created successfully.")

except Exception as e:
    print(f"Error during database ingestion: {e}")

print("\n" + "="*50 + "\n")

# -------------------------------------------------------------
# TASK 2: Execute Executive SQL Queries
# -------------------------------------------------------------
print("--- Executing Executive SQL Queries ---\n")

# Query 1: Top Product Categories by Total Revenue & Average Order Value
query_top_categories = """
SELECT 
    Product_Category,
    COUNT(User_ID) AS Total_Transactions,
    SUM(Orders) AS Total_Orders,
    ROUND(SUM(Amount), 2) AS Total_Revenue,
    ROUND(AVG(Amount), 2) AS Avg_Order_Value
FROM fact_transactions
GROUP BY Product_Category
ORDER BY Total_Revenue DESC;
"""

print("Query 1: Category Performance Summary")
df_res1 = pd.read_sql_query(query_top_categories, conn)
print(df_res1.to_string(index=False))

print("\n" + "-"*50 + "\n")

# Query 2: Annual Vehicle Registrations Highlighting Festival Months (Oct-Nov)
query_vahan_trend = """
SELECT 
    Year,
    SUM(CASE WHEN Month_Num IN (10, 11) THEN Total_Registrations ELSE 0 END) AS Festive_Registrations,
    SUM(Total_Registrations) AS Total_Yearly_Registrations,
    ROUND(CAST(SUM(CASE WHEN Month_Num IN (10, 11) THEN Total_Registrations ELSE 0 END) AS REAL) / SUM(Total_Registrations) * 100, 2) AS Festive_Share_Percent
FROM fact_vehicle_registrations
GROUP BY Year
ORDER BY Year;
"""

print("Query 2: Annual Vehicle Registrations & Festive Share (2020-2025)")
df_res2 = pd.read_sql_query(query_vahan_trend, conn)
print(df_res2.to_string(index=False))

# Close connection
conn.close()
print("\nDatabase connection closed successfully.")