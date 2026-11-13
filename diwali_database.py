
import pandas as pd
import sqlite3
from pathlib import Path

print("=" * 65)
print("SPRINT 3: RELATIONAL DATABASE & SQL ANALYTICS")
print("=" * 65)

# -------------------------------------------------------------
# PROJECT PATHS
# -------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = BASE_DIR / "diwali_economy.db"


# -------------------------------------------------------------
# COMMON FUNCTION: LOAD CSV OR EXCEL
# -------------------------------------------------------------

def load_dataset(filename_base, encoding="latin1"):

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
            f"Dataset not found: {filename_base}"
        )


# -------------------------------------------------------------
# TASK 1: PREPARE SALES DATA
# -------------------------------------------------------------

def prepare_sales_data():

    print("\n--- 1. Preparing Diwali Sales Data ---")

    cleaned_path = OUTPUT_DIR / "diwali_sales_cleaned.csv"

    if cleaned_path.exists():

        df = pd.read_csv(cleaned_path, encoding="latin1")
        print("Using cleaned sales dataset from Sprint 2.")

    else:

        print("Cleaned dataset unavailable. Loading original data.")

        df = load_dataset("Diwali Sales Data")

        df = df.drop_duplicates().copy()

        required_columns = [
            "User_ID",
            "Product_Category",
            "Amount"
        ]

        missing = [
            col for col in required_columns
            if col not in df.columns
        ]

        if missing:
            raise ValueError(
                f"Missing required sales columns: {missing}"
            )

        df["Amount"] = pd.to_numeric(
            df["Amount"], errors="coerce"
        )

        category_median = df.groupby(
            "Product_Category"
        )["Amount"].transform("median")

        df["Amount"] = df["Amount"].fillna(category_median)

        if df["Amount"].isnull().any():
            df["Amount"] = df["Amount"].fillna(
                df["Amount"].median()
            )

    required_columns = [
        "User_ID",
        "Product_Category",
        "Amount"
    ]

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required sales columns: {missing}"
        )

    df["Amount"] = pd.to_numeric(
        df["Amount"], errors="coerce"
    )

    df = df.dropna(
        subset=["User_ID", "Product_Category", "Amount"]
    ).copy()

    if "Orders" in df.columns:
        df["Orders"] = pd.to_numeric(
            df["Orders"], errors="coerce"
        )

    print(f"Sales records prepared: {len(df)}")

    return df


# -------------------------------------------------------------
# TASK 2: PREPARE VAHAN DATA
# -------------------------------------------------------------

def prepare_vahan_data():

    print("\n--- 2. Preparing VAHAN Registration Data ---")

    cleaned_path = OUTPUT_DIR / "vahan_monthly_cleaned.csv"

    if cleaned_path.exists():

        df = pd.read_csv(cleaned_path)
        print("Using cleaned VAHAN dataset from Sprint 2.")

    else:

        print("Cleaned dataset unavailable. Loading original files.")

        df_m1 = load_dataset(
            "2020-2022 montwise vahan"
        ).iloc[:, :2].copy()

        df_m2 = load_dataset(
            "2023-2025 montiwse vahan"
        ).iloc[:, :2].copy()

        df_m1.columns = [
            "Month", "Total_Registrations"
        ]

        df_m2.columns = [
            "Month", "Total_Registrations"
        ]

        df = pd.concat(
            [df_m1, df_m2],
            ignore_index=True
        )

    required_columns = [
        "Month", "Total_Registrations"
    ]

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing VAHAN columns: {missing}"
        )

    df["Month_DT"] = pd.to_datetime(
        df["Month"].astype(str).str.strip(),
        format="%Y-%m",
        errors="coerce"
    )

    df["Total_Registrations"] = pd.to_numeric(
        df["Total_Registrations"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["Month_DT", "Total_Registrations"]
    ).copy()

    # Remove duplicate months
    df = df.drop_duplicates(
        subset=["Month_DT"],
        keep="last"
    )

    df = df.sort_values(
        "Month_DT"
    ).reset_index(drop=True)

    df["Year"] = df["Month_DT"].dt.year
    df["Month_Num"] = df["Month_DT"].dt.month

    # October-November indicator, not an exact Diwali indicator
    df["Is_Oct_Nov"] = df["Month_Num"].isin([10, 11]).astype(int)

    print(f"VAHAN records prepared: {len(df)}")

    return df


# -------------------------------------------------------------
# TASK 3: CREATE SQLITE DATABASE
# -------------------------------------------------------------

def create_database(conn, df_sales, df_vahan):

    print("\n--- 3. Creating SQLite Tables ---")

    with conn:

        df_sales.to_sql(
            "fact_transactions",
            conn,
            if_exists="replace",
            index=False
        )

        df_vahan.to_sql(
            "fact_vehicle_registrations",
            conn,
            if_exists="replace",
            index=False
        )

        # Indexes improve filtering and grouping performance
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_sales_category
            ON fact_transactions(Product_Category);
        """)

        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_sales_user
            ON fact_transactions(User_ID);
        """)

        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_vahan_year
            ON fact_vehicle_registrations(Year);
        """)

    print("Table created: fact_transactions")
    print("Table created: fact_vehicle_registrations")


# -------------------------------------------------------------
# TASK 4: EXECUTIVE SQL ANALYTICS
# -------------------------------------------------------------

def execute_sql_analytics(conn):

    print("\n--- 4. Executing Executive SQL Queries ---")

    queries = {

        # QUERY 1: Product Category Performance
        "category_performance": """
            SELECT
                Product_Category,

                COUNT(*) AS Total_Records,

                COUNT(DISTINCT User_ID) AS Unique_Customers,

                ROUND(SUM(Amount), 2) AS Total_Recorded_Sales,

                ROUND(AVG(Amount), 2) AS Avg_Recorded_Amount,

                ROUND(MIN(Amount), 2) AS Minimum_Amount,

                ROUND(MAX(Amount), 2) AS Maximum_Amount

            FROM fact_transactions

            GROUP BY Product_Category

            ORDER BY Total_Recorded_Sales DESC;
        """,

        # QUERY 2: Customer Purchase Activity
        "customer_activity": """
            SELECT
                User_ID,

                COUNT(*) AS Purchase_Records,

                COUNT(DISTINCT Product_Category) AS Categories_Purchased,

                ROUND(SUM(Amount), 2) AS Total_Recorded_Spending,

                ROUND(AVG(Amount), 2) AS Avg_Recorded_Amount

            FROM fact_transactions

            GROUP BY User_ID

            ORDER BY Total_Recorded_Spending DESC

            LIMIT 20;
        """,

        # QUERY 3: Annual Vehicle Registration Trend
        "annual_vehicle_trend": """
            SELECT
                Year,

                SUM(Total_Registrations) AS Annual_Registrations,

                SUM(
                    CASE
                        WHEN Month_Num IN (10, 11)
                        THEN Total_Registrations
                        ELSE 0
                    END
                ) AS Oct_Nov_Registrations,

                ROUND(
                    100.0 *
                    SUM(
                        CASE
                            WHEN Month_Num IN (10, 11)
                            THEN Total_Registrations
                            ELSE 0
                        END
                    ) /
                    NULLIF(SUM(Total_Registrations), 0),
                    2
                ) AS Oct_Nov_Share_Percent

            FROM fact_vehicle_registrations

            GROUP BY Year

            ORDER BY Year;
        """,

        # QUERY 4: Monthly Vehicle Registration Trend
        "monthly_vehicle_trend": """
            SELECT
                Year,
                Month_Num,

                SUM(Total_Registrations) AS Monthly_Registrations

            FROM fact_vehicle_registrations

            GROUP BY Year, Month_Num

            ORDER BY Year, Month_Num;
        """
    }

    for query_name, query in queries.items():

        print("\n" + "-" * 65)
        print(f"QUERY: {query_name.upper()}")
        print("-" * 65)

        result = pd.read_sql_query(
            query,
            conn
        )

        print(result.to_string(index=False))

        # Export SQL results
        output_path = OUTPUT_DIR / f"{query_name}.csv"

        result.to_csv(
            output_path,
            index=False
        )

        print(f"\nExported: {output_path.name}")


# -------------------------------------------------------------
# TASK 5: DATABASE VALIDATION
# -------------------------------------------------------------

def validate_database(conn):

    print("\n--- 5. Database Validation ---")

    tables = pd.read_sql_query(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name;
        """,
        conn
    )

    print("\nAvailable Tables:")
    print(tables.to_string(index=False))

    for table in tables["name"]:

        count = pd.read_sql_query(
            f'SELECT COUNT(*) AS Total_Rows FROM "{table}"',
            conn
        ).iloc[0]["Total_Rows"]

        print(f"{table}: {count} rows")


# -------------------------------------------------------------
# MAIN EXECUTION
# -------------------------------------------------------------

def main():

    conn = None

    try:

        print(f"\nDatabase: {DB_PATH}")

        df_sales = prepare_sales_data()

        df_vahan = prepare_vahan_data()

        conn = sqlite3.connect(DB_PATH)

        print("\nSQLite connection established.")

        create_database(
            conn,
            df_sales,
            df_vahan
        )

        execute_sql_analytics(conn)

        validate_database(conn)

        print("\n" + "=" * 65)
        print("SPRINT 3 COMPLETED SUCCESSFULLY")
        print("=" * 65)

        print("\nGenerated Files:")
        print("- diwali_economy.db")
        print("- category_performance.csv")
        print("- customer_activity.csv")
        print("- annual_vehicle_trend.csv")
        print("- monthly_vehicle_trend.csv")

    except Exception as e:

        print(f"\nERROR: Sprint 3 failed: {e}")

    finally:

        if conn is not None:
            conn.close()
            print("\nDatabase connection closed.")


if __name__ == "__main__":
    main()
