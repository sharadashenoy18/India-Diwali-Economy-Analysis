import pandas as pd
import os

print("=== SPRINT 2: DATA CLEANING & FEATURE ENGINEERING ===\n")

# -------------------------------------------------------------
# TASK 1: Clean Kaggle Diwali Sales Dataset
# -------------------------------------------------------------
print("--- 1. Cleaning Kaggle Diwali Sales Data ---")
try:
    if os.path.exists('Diwali Sales Data.csv'):
        df_sales = pd.read_csv('Diwali Sales Data.csv', encoding='latin1')
    else:
        df_sales = pd.read_excel('Diwali Sales Data.xlsx')
        
    initial_rows = len(df_sales)
    
    # Drop exact duplicates
    df_sales = df_sales.drop_duplicates()
    
    # Handle missing values in 'Amount' by filling with the median of their respective Product_Category
    df_sales['Amount'] = df_sales['Amount'].fillna(df_sales.groupby('Product_Category')['Amount'].transform('median'))
    
    print(f"Original Row Count: {initial_rows}")
    print(f"Cleaned Row Count: {len(df_sales)} (Removed {initial_rows - len(df_sales)} duplicates)")
    print(f"Remaining Missing Values in Amount: {df_sales['Amount'].isnull().sum()}")

except Exception as e:
    print(f"Error cleaning sales data: {e}")

print("\n" + "="*50 + "\n")

# -------------------------------------------------------------
# TASK 2: Feature Engineering on VAHAN Monthly Data
# -------------------------------------------------------------
print("--- 2. Feature Engineering on VAHAN Monthly Data ---")
try:
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
    
    # Feature Engineering: Create a Festival Window Flag (Oct & Nov as core festival window)
    df_vahan['Is_Festival_Month'] = df_vahan['Month_Num'].isin([10, 11])
    
    # Compare average registrations during festival months vs non-festival months
    festive_comparison = df_vahan.groupby('Is_Festival_Month')['Total_Registrations'].mean().reset_index()
    festive_comparison['Period'] = festive_comparison['Is_Festival_Month'].map({True: 'Festival (Oct-Nov)', False: 'Non-Festival'})
    
    print("Average Monthly Vehicle Registrations Comparison:")
    print(festive_comparison[['Period', 'Total_Registrations']].to_string(index=False))

except Exception as e:
    print(f"Error in VAHAN feature engineering: {e}")

print("\n" + "="*50 + "\n")

# -------------------------------------------------------------
# TASK 3: Extract India Jewellery Demand from WGC Data
# -------------------------------------------------------------
print("--- 3. Extracting India Jewellery Demand (World Gold Council) ---")
try:
    excel_path = 'GDT Tables_Q326_EN.xlsx'
    df_jewellery = pd.read_excel(excel_path, sheet_name='Jewellery')
    
    # Search for the row where India data is located
    # Typically WGC tables have countries in a column and years across headers
    print("Successfully accessed World Gold Council Jewellery Sheet.")
    print(f"Dimensions: {df_jewellery.shape}")

except Exception as e:
    print(f"Error extracting World Gold Council data: {e}")