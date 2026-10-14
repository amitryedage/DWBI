"""Star Schema Data Warehouse Builder for E-Commerce Customer Analytics Dashboard.

Transforms cleaned analytical dataset into a relational Star Schema:
- dim_customer (Dimension: Who)
- dim_product  (Dimension: What)
- dim_date     (Dimension: When)
- fact_orders  (Fact: Transactional Measures)

Generates surrogate integer keys and exports normalized CSVs to data/processed/.
"""

from pathlib import Path
import pandas as pd
from src.config import (
    CLEAN_PARQUET_PATH,
    FACT_ORDERS_PATH,
    DIM_CUSTOMER_PATH,
    DIM_PRODUCT_PATH,
    DIM_DATE_PATH,
    PROCESSED_DATA_DIR,
)
from src.clean import clean_ecommerce_data, is_festive_season


def build_star_schema(df_clean: pd.DataFrame = None):
    """Generate fact and dimension tables with surrogate keys."""
    print("=" * 60)
    print("DATA WAREHOUSE STAR SCHEMA MODELING")
    print("=" * 60)

    if df_clean is None:
        if CLEAN_PARQUET_PATH.exists():
            print(f"Loading cleaned data from: {CLEAN_PARQUET_PATH}")
            df_clean = pd.read_parquet(CLEAN_PARQUET_PATH)
        else:
            print("Cleaned parquet not found. Running cleansing pipeline first...")
            df_clean = clean_ecommerce_data()

    # Ensure Date is datetime
    df_clean["Order_Date"] = pd.to_datetime(df_clean["Order_Date"])

    # -------------------------------------------------------------
    # 1. dim_customer (Dimension: Who)
    # -------------------------------------------------------------
    print("[1/4] Building dim_customer...")
    # Deduplicate customers by Customer_ID, taking the latest record if attributes changed
    cust_cols = [
        "Customer_ID",
        "Customer_Name",
        "Gender",
        "Age",
        "Age_Group",
        "City",
        "State",
        "Customer_Segment",
    ]
    dim_customer = (
        df_clean.sort_values("Order_Date", ascending=True)
        .groupby("Customer_ID")[cust_cols]
        .last()
        .reset_index(drop=True)
    )
    dim_customer.insert(0, "Customer_Key", range(1, len(dim_customer) + 1))
    print(f"      dim_customer created: {len(dim_customer):,} unique customers.")

    # -------------------------------------------------------------
    # 2. dim_product (Dimension: What)
    # -------------------------------------------------------------
    print("[2/4] Building dim_product...")
    dim_product = (
        df_clean[["Product_Name", "Product_Category"]]
        .drop_duplicates()
        .sort_values(["Product_Category", "Product_Name"])
        .reset_index(drop=True)
    )
    dim_product.insert(0, "Product_Key", range(1, len(dim_product) + 1))
    print(f"      dim_product created: {len(dim_product):,} unique products.")

    # -------------------------------------------------------------
    # 3. dim_date (Dimension: When)
    # -------------------------------------------------------------
    print("[3/4] Building dim_date...")
    min_date = df_clean["Order_Date"].min()
    max_date = df_clean["Order_Date"].max()
    all_dates = pd.date_range(min_date, max_date, freq="D")

    dim_date = pd.DataFrame({"Date": all_dates})
    dim_date["Date_Key"] = dim_date["Date"].dt.strftime("%Y%m%d").astype(int)
    dim_date["Day"] = dim_date["Date"].dt.day
    dim_date["Month"] = dim_date["Date"].dt.month
    dim_date["Month_Name"] = dim_date["Date"].dt.strftime("%b")
    dim_date["Quarter"] = "Q" + dim_date["Date"].dt.quarter.astype(str)
    dim_date["Year"] = dim_date["Date"].dt.year
    dim_date["Is_Festive_Season"] = dim_date["Date"].apply(is_festive_season)

    # Reorder columns with Date_Key first
    date_cols = ["Date_Key", "Date", "Day", "Month", "Month_Name", "Quarter", "Year", "Is_Festive_Season"]
    dim_date = dim_date[date_cols]
    print(f"      dim_date created: {len(dim_date):,} dates ({min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}).")

    # -------------------------------------------------------------
    # 4. fact_orders (Fact Table: Measurable business events)
    # -------------------------------------------------------------
    print("[4/4] Building fact_orders and linking foreign keys...")
    
    # Map foreign keys
    cust_key_map = dict(zip(dim_customer["Customer_ID"], dim_customer["Customer_Key"]))
    prod_key_map = dict(zip(dim_product["Product_Name"], dim_product["Product_Key"]))
    
    fact_orders = df_clean.copy()
    fact_orders["Customer_Key"] = fact_orders["Customer_ID"].map(cust_key_map)
    fact_orders["Product_Key"] = fact_orders["Product_Name"].map(prod_key_map)
    fact_orders["Date_Key"] = fact_orders["Order_Date"].dt.strftime("%Y%m%d").astype(int)

    # Select fact table columns
    fact_cols = [
        "Order_ID",
        "Customer_Key",
        "Product_Key",
        "Date_Key",
        "Quantity",
        "Unit_Price",
        "Discount_Pct",
        "Total_Amount",
        "Order_Status",
        "Payment_Method",
        "Device_Type",
        "Delivery_Days",
        "Customer_Rating",
        "Net_Flag",
    ]
    fact_orders = fact_orders[fact_cols]

    # Referential Integrity Verification
    assert fact_orders["Customer_Key"].notnull().all(), "Unmapped Customer_Key in fact_orders!"
    assert fact_orders["Product_Key"].notnull().all(), "Unmapped Product_Key in fact_orders!"
    assert fact_orders["Date_Key"].isin(dim_date["Date_Key"]).all(), "Unmapped Date_Key in fact_orders!"
    print(f"      fact_orders created: {len(fact_orders):,} rows with 100% referential integrity.")

    # -------------------------------------------------------------
    # 5. Export CSV files
    # -------------------------------------------------------------
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    fact_orders.to_csv(FACT_ORDERS_PATH, index=False)
    dim_customer.to_csv(DIM_CUSTOMER_PATH, index=False)
    dim_product.to_csv(DIM_PRODUCT_PATH, index=False)
    dim_date.to_csv(DIM_DATE_PATH, index=False)

    print("=" * 60)
    print("STAR SCHEMA EXPORTS COMPLETED:")
    print(f"  Fact:       {FACT_ORDERS_PATH.name} ({len(fact_orders):,} rows)")
    print(f"  Dimension:  {DIM_CUSTOMER_PATH.name} ({len(dim_customer):,} rows)")
    print(f"  Dimension:  {DIM_PRODUCT_PATH.name} ({len(dim_product):,} rows)")
    print(f"  Dimension:  {DIM_DATE_PATH.name} ({len(dim_date):,} rows)")
    print("=" * 60)

    return {
        "fact_orders": fact_orders,
        "dim_customer": dim_customer,
        "dim_product": dim_product,
        "dim_date": dim_date,
    }


if __name__ == "__main__":
    build_star_schema()
