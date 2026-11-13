
import pandas as pd
import os
from pathlib import Path

print("=" * 65)
print("SPRINT 2: DATA CLEANING & FEATURE ENGINEERING")
print("=" * 65)

# -------------------------------------------------------------
# PROJECT PATHS
# -------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# -------------------------------------------------------------
# COMMON FUNCTION: LOAD CSV OR EXCEL
# -------------------------------------------------------------

def load_dataset(filename_base, encoding="latin1"):
    """
    Loads a CSV or Excel dataset.
    CSV is preferred when both formats exist.
    """

    csv_path = BASE_DIR / f"{filename_base}.csv"
    excel_path = BASE_DIR / f"{filename_base}.xlsx"

    if csv_path.exists():
        print(f"Loading: {csv_path.name}")
        return pd.read_csv(csv_path, encoding=encoding)

    elif excel_path.exists():
        print(f"Loading: {excel_path.name}")
        return pd.read_excel(excel_path)

    else:
        raise FileNotFoundError(
            f"Neither {csv_path.name} nor {excel_path.name} was found."
        )


# -------------------------------------------------------------
# TASK 1: CLEAN KAGGLE DIWALI SALES DATASET
# -------------------------------------------------------------

def clean_diwali_sales():

    print("\n--- 1. Cleaning Kaggle Diwali Sales Data ---")

    try:
        df = load_dataset("Diwali Sales Data")

        initial_rows = len(df)

        # Remove exact duplicate records
        df = df.drop_duplicates().copy()

        # Convert Amount into numeric format
        df["Amount"] = pd.to_numeric(
            df["Amount"], errors="coerce"
        )

        # Fill missing Amount values using Product_Category median
        if "Product_Category" in df.columns:

            category_medians = df.groupby(
                "Product_Category"
            )["Amount"].transform("median")

            df["Amount"] = df["Amount"].fillna(category_medians)

        # Fallback: use overall median if category median is unavailable
        if df["Amount"].isnull().any():

            overall_median = df["Amount"].median()

            if pd.notna(overall_median):
                df["Amount"] = df["Amount"].fillna(overall_median)

        # Save cleaned dataset
        output_path = OUTPUT_DIR / "diwali_sales_cleaned.csv"

        df.to_csv(output_path, index=False)

        print(f"Original rows       : {initial_rows}")
        print(f"Cleaned rows        : {len(df)}")
        print(f"Duplicates removed  : {initial_rows - len(df)}")
        print(
            "Missing Amount      :",
            df["Amount"].isnull().sum()
        )
        print(f"Saved successfully  : {output_path}")

        return df

    except Exception as e:
        print(f"Error cleaning Diwali Sales data: {e}")
        return None


# -------------------------------------------------------------
# TASK 2: VAHAN DATA CLEANING & FEATURE ENGINEERING
# -------------------------------------------------------------

def clean_vahan_data():

    print("\n--- 2. VAHAN Data Cleaning & Feature Engineering ---")

    try:

        # Load the two VAHAN datasets
        df_m1 = load_dataset(
            "2020-2022 montwise vahan"
        )

        df_m2 = load_dataset(
            "2023-2025 montiwse vahan"
        )

        # Retain the first two columns as in the original source
        df_m1 = df_m1.iloc[:, :2].copy()
        df_m2 = df_m2.iloc[:, :2].copy()

        df_m1.columns = ["Month", "Total_Registrations"]
        df_m2.columns = ["Month", "Total_Registrations"]

        # Combine both datasets
        df = pd.concat(
            [df_m1, df_m2],
            ignore_index=True
        )

        # Clean month values
        df["Month"] = df["Month"].astype(str).str.strip()

        # Convert registrations to numeric
        df["Total_Registrations"] = pd.to_numeric(
            df["Total_Registrations"],
            errors="coerce"
        )

        # Retain valid YYYY-MM dates
        valid_month = df["Month"].str.fullmatch(
            r"\d{4}-\d{2}"
        )

        df = df.loc[valid_month].copy()

        # Convert month into datetime
        df["Month_DT"] = pd.to_datetime(
            df["Month"],
            format="%Y-%m",
            errors="coerce"
        )

        # Remove invalid records
        df = df.dropna(
            subset=["Month_DT", "Total_Registrations"]
        )

        # Remove duplicate months
        df = df.drop_duplicates(
            subset=["Month_DT"],
            keep="last"
        )

        # Sort chronologically
        df = df.sort_values("Month_DT").reset_index(drop=True)

        # Feature Engineering
        df["Year"] = df["Month_DT"].dt.year
        df["Month_Num"] = df["Month_DT"].dt.month
        df["Month_Name"] = df["Month_DT"].dt.month_name()

        # October-November indicator.
        # This is NOT an exact Diwali indicator because Diwali dates
        # change every year and may fall in October or November.
        df["Is_Oct_Nov"] = df["Month_Num"].isin([10, 11])

        # Save cleaned VAHAN data
        output_path = OUTPUT_DIR / "vahan_monthly_cleaned.csv"

        df.to_csv(output_path, index=False)

        # Compare October-November with other months
        comparison = (
            df.groupby("Is_Oct_Nov")["Total_Registrations"]
            .agg(["mean", "median", "count"])
            .reset_index()
        )

        comparison["Period"] = comparison["Is_Oct_Nov"].map({
            True: "October-November",
            False: "Other Months"
        })

        comparison = comparison[
            ["Period", "mean", "median", "count"]
        ]

        print("\nMonthly Vehicle Registration Comparison:")
        print(comparison.to_string(index=False))

        print(f"\nTotal valid records: {len(df)}")
        print(f"Saved successfully : {output_path}")

        return df

    except Exception as e:
        print(f"Error processing VAHAN data: {e}")
        return None


# -------------------------------------------------------------
# TASK 3: WORLD GOLD COUNCIL JEWELLERY DATA
# -------------------------------------------------------------

def extract_india_jewellery_data():

    print("\n--- 3. World Gold Council Jewellery Data ---")

    try:

        excel_path = BASE_DIR / "GDT Tables_Q326_EN.xlsx"

        if not excel_path.exists():
            raise FileNotFoundError(
                f"File not found: {excel_path.name}"
            )

        # Read Jewellery worksheet
        df = pd.read_excel(
            excel_path,
            sheet_name="Jewellery"
        )

        print(f"Original dimensions: {df.shape}")

        # Search all columns for rows containing India
        india_mask = df.astype(str).apply(
            lambda column: column.str.contains(
                r"\bIndia\b",
                case=False,
                na=False,
                regex=True
            )
        ).any(axis=1)

        df_india = df.loc[india_mask].copy()

        if df_india.empty:

            print(
                "No rows containing 'India' were detected."
            )

            print(
                "Inspect the Jewellery worksheet structure "
                "before extracting country-level figures."
            )

            return None

        # Save India-related rows
        output_path = OUTPUT_DIR / "india_jewellery_demand_raw.csv"

        df_india.to_csv(
            output_path,
            index=False
        )

        print(f"India-related rows: {len(df_india)}")
        print("\nExtracted data preview:")
        print(df_india.head(10).to_string(index=False))

        print(f"\nSaved successfully: {output_path}")

        return df_india

    except Exception as e:

        print(f"Error extracting WGC data: {e}")
        return None


# -------------------------------------------------------------
# MAIN EXECUTION
# -------------------------------------------------------------

if __name__ == "__main__":

    sales_data = clean_diwali_sales()

    print("\n" + "=" * 65)

    vahan_data = clean_vahan_data()

    print("\n" + "=" * 65)

    jewellery_data = extract_india_jewellery_data()

    print("\n" + "=" * 65)
    print("SPRINT 2 EXECUTION COMPLETED")
    print("=" * 65)

    print("\nCheck the 'output' folder for generated datasets.")
