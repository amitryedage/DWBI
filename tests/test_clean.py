"""Unit tests for Phase 2 Data Cleansing and Star Schema Warehouse Modeling.

Tests:
- Row count after deduplication is exactly 9,900
- No duplicate Order_IDs
- Required columns have zero nulls
- Missing value imputation rules applied correctly
- Value ranges are strictly valid
- Derived columns exist and have correct formats
- Star schema tables exist and maintain 100% referential integrity
"""

import pytest
import pandas as pd
from pathlib import Path
from src.config import (
    CLEAN_PARQUET_PATH,
    CLEAN_EXCEL_PATH,
    FACT_ORDERS_PATH,
    DIM_CUSTOMER_PATH,
    DIM_PRODUCT_PATH,
    DIM_DATE_PATH,
)


@pytest.fixture(scope="module")
def clean_df():
    """Load cleaned parquet dataset."""
    assert CLEAN_PARQUET_PATH.exists(), f"Cleaned parquet not found at {CLEAN_PARQUET_PATH}"
    df = pd.read_parquet(CLEAN_PARQUET_PATH)
    return df


@pytest.fixture(scope="module")
def star_schema():
    """Load star schema CSV files."""
    assert FACT_ORDERS_PATH.exists(), "fact_orders.csv missing"
    assert DIM_CUSTOMER_PATH.exists(), "dim_customer.csv missing"
    assert DIM_PRODUCT_PATH.exists(), "dim_product.csv missing"
    assert DIM_DATE_PATH.exists(), "dim_date.csv missing"

    return {
        "fact": pd.read_csv(FACT_ORDERS_PATH),
        "cust": pd.read_csv(DIM_CUSTOMER_PATH),
        "prod": pd.read_csv(DIM_PRODUCT_PATH),
        "date": pd.read_csv(DIM_DATE_PATH),
    }


def test_row_count(clean_df):
    """Cleaned dataset must contain exactly 9,900 rows after removing 100 duplicates."""
    assert len(clean_df) == 9900, f"Expected 9,900 rows, got {len(clean_df)}"


def test_no_duplicate_orders(clean_df):
    """Order_ID must be unique across all rows."""
    assert clean_df["Order_ID"].nunique() == 9900
    assert clean_df["Order_ID"].duplicated().sum() == 0


def test_no_nulls_in_required_columns(clean_df):
    """Critical columns must have 0 null values after imputation."""
    required_cols = [
        "Order_ID",
        "Order_Date",
        "Customer_ID",
        "Customer_Name",
        "Gender",
        "Age",
        "City",
        "State",
        "Customer_Segment",
        "Product_Category",
        "Product_Name",
        "Unit_Price",
        "Quantity",
        "Discount_Pct",
        "Total_Amount",
        "Payment_Method",
        "Order_Status",
        "Device_Type",
        "Age_Imputed",
        "Net_Flag",
        "Age_Group",
        "Discount_Band",
    ]
    for col in required_cols:
        null_count = clean_df[col].isna().sum()
        assert null_count == 0, f"Column '{col}' unexpectedly has {null_count} nulls!"


def test_valid_ranges(clean_df):
    """Validate numerical boundary conditions."""
    assert clean_df["Age"].between(18, 70).all(), "Age out of range [18, 70]"
    assert clean_df["Discount_Pct"].between(0, 40).all(), "Discount out of range [0, 40]"
    assert (clean_df["Quantity"] >= 1).all(), "Quantity must be >= 1"
    assert (clean_df["Unit_Price"] > 0).all(), "Unit_Price must be > 0"
    
    # Rating range for non-null reviews
    ratings = clean_df["Customer_Rating"].dropna()
    assert ratings.between(1.0, 5.0).all(), "Customer_Rating out of range [1, 5]"


def test_legitimate_blanks(clean_df):
    """Delivery_Days must be blank for Cancelled and Shipped orders."""
    unfulfilled = clean_df[clean_df["Order_Status"].isin(["Cancelled", "Shipped"])]
    assert unfulfilled["Delivery_Days"].isna().all(), "Cancelled/Shipped orders must have null Delivery_Days"


def test_total_amount_calculation(clean_df):
    """Recalculated Total_Amount must match within 0.01 INR."""
    expected = clean_df["Unit_Price"] * clean_df["Quantity"] * (1 - clean_df["Discount_Pct"] / 100)
    diff = (clean_df["Total_Amount"] - expected).abs()
    assert (diff <= 0.01).all(), "Total_Amount calculation mismatch found!"


def test_derived_columns(clean_df):
    """Validate derived dimensions."""
    assert set(clean_df["Year"].unique()) == {2024, 2025}
    assert clean_df["Month"].between(1, 12).all()
    assert set(clean_df["Quarter"].unique()) == {"Q1", "Q2", "Q3", "Q4"}
    
    expected_age_groups = {"<25", "25-34", "35-49", "50+"}
    assert set(clean_df["Age_Group"].unique()).issubset(expected_age_groups)
    
    # Net_Flag accuracy
    delivered_shipped = clean_df["Order_Status"].isin(["Delivered", "Shipped"])
    assert (clean_df["Net_Flag"] == delivered_shipped).all()


def test_star_schema_referential_integrity(star_schema):
    """Validate fact table foreign keys map to dimension tables with zero orphan keys."""
    fact = star_schema["fact"]
    cust = star_schema["cust"]
    prod = star_schema["prod"]
    date = star_schema["date"]

    assert len(fact) == 9900
    assert len(cust) == 2424
    assert len(prod) == 40
    assert len(date) == 731

    # Referential checks
    assert fact["Customer_Key"].isin(cust["Customer_Key"]).all(), "Orphan Customer_Key in fact table!"
    assert fact["Product_Key"].isin(prod["Product_Key"]).all(), "Orphan Product_Key in fact table!"
    assert fact["Date_Key"].isin(date["Date_Key"]).all(), "Orphan Date_Key in fact table!"
