"""Data Cleaning & ETL Pipeline for E-Commerce Customer Analytics Dashboard.

Notice Phase 2:
- Loads raw dataset from data/raw/ecommerce_data.xlsx
- Strips whitespace & enforces strict data types
- Purges exact duplicate records (100 rows -> 9,900 clean rows)
- Imputes missing values per documented business rules (Gender, Age, City, Payment_Method)
- Validates numerical boundary conditions (Age 18-70, Discount 0-40, Rating 1-5, Quantity >= 1)
- Validates Total_Amount formula consistency (within 0.01 tolerance)
- Engineers derived features: Year, Month, Month_Name, Quarter, Year_Month, Net_Flag,
  Age_Group, Discount_Band, Is_Festive_Season
- Exports clean datasets to data/processed/ (Parquet & Excel)
"""

from pathlib import Path
import pandas as pd
import numpy as np
from src.config import RAW_DATA_PATH, CLEAN_PARQUET_PATH, CLEAN_EXCEL_PATH, PROCESSED_DATA_DIR


def classify_age_group(age: float) -> str:
    """Classify age into demographic cohorts."""
    if pd.isna(age):
        return "Unknown"
    elif age < 25:
        return "<25"
    elif age <= 34:
        return "25-34"
    elif age <= 49:
        return "35-49"
    else:
        return "50+"


def classify_discount_band(pct: float) -> str:
    """Classify discount percentage into promotional bands."""
    if pd.isna(pct) or pct == 0:
        return "No Discount (0%)"
    elif pct <= 10:
        return "Low (1-10%)"
    elif pct <= 20:
        return "Medium (11-20%)"
    elif pct <= 30:
        return "High (21-30%)"
    else:
        return "Very High (>30%)"


def is_festive_season(order_date: pd.Timestamp) -> bool:
    """Check if date falls in Indian festive season (mid-October to mid-November)."""
    # Oct 15 to Nov 15
    month, day = order_date.month, order_date.day
    if (month == 10 and day >= 15) or (month == 11 and day <= 15):
        return True
    return False


def clean_ecommerce_data(raw_path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    """Execute complete cleansing pipeline and return cleaned DataFrame."""
    print("=" * 60)
    print("PHASE 2 DATA CLEANSING & PREPARATION PIPELINE")
    print("=" * 60)
    print(f"[1/7] Loading raw data from: {raw_path}")
    
    xl = pd.ExcelFile(raw_path)
    df = xl.parse("Orders_Data")
    rows_in = len(df)
    print(f"      Initial row count: {rows_in:,}")

    # Step 1: Trim all string columns
    print("[2/7] Trimming whitespace & standardizing text fields...")
    str_cols = df.select_dtypes(include=["object"]).columns
    for c in str_cols:
        df[c] = df[c].astype(str).str.strip()
        # Convert literal 'nan', 'None' back to np.nan
        df[c] = df[c].replace({"nan": np.nan, "None": np.nan, "": np.nan})

    # Step 2: Remove exact duplicate rows
    print("[3/7] Deduplicating records...")
    dup_mask = df.duplicated()
    dup_count = dup_mask.sum()
    df = df.drop_duplicates().reset_index(drop=True)
    print(f"      Purged {dup_count} exact duplicate rows. Retained: {len(df):,}")

    # Step 3: Handle missing values per documented rules
    print("[4/7] Imputing missing values per business rules...")
    # Gender -> 'Unknown'
    gender_missing = df["Gender"].isna().sum()
    df["Gender"] = df["Gender"].fillna("Unknown")

    # City -> 'Unknown'
    city_missing = df["City"].isna().sum()
    df["City"] = df["City"].fillna("Unknown")

    # Payment_Method -> 'Unknown'
    pm_missing = df["Payment_Method"].isna().sum()
    df["Payment_Method"] = df["Payment_Method"].fillna("Unknown")

    # Age -> Impute with median and set flag
    age_missing = df["Age"].isna().sum()
    median_age = float(df["Age"].median())
    df["Age_Imputed"] = df["Age"].isna()
    df["Age"] = df["Age"].fillna(median_age).astype(int)

    # Delivery_Days & Customer_Rating:
    # Deliberately preserved as NaN for unfulfilled / unreviewed orders
    delivery_blank = df["Delivery_Days"].isna().sum()
    rating_blank = df["Customer_Rating"].isna().sum()

    print(f"      - Gender filled with 'Unknown': {gender_missing:,}")
    print(f"      - Age filled with median ({median_age:.0f}) + Age_Imputed flag: {age_missing:,}")
    print(f"      - City filled with 'Unknown': {city_missing:,}")
    print(f"      - Payment_Method filled with 'Unknown': {pm_missing:,}")
    print(f"      - Delivery_Days preserved blank (unfulfilled): {delivery_blank:,}")
    print(f"      - Customer_Rating preserved blank (unreviewed): {rating_blank:,}")

    # Step 4: Validate boundaries & types
    print("[5/7] Validating types, ranges and business logic...")
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df["Unit_Price"] = df["Unit_Price"].astype(float)
    df["Quantity"] = df["Quantity"].astype(int)
    df["Discount_Pct"] = df["Discount_Pct"].astype(float)
    df["Total_Amount"] = df["Total_Amount"].astype(float)

    # Range assertions
    assert (df["Age"] >= 18).all() and (df["Age"] <= 70).all(), "Age out of range [18, 70]"
    assert (df["Discount_Pct"] >= 0).all() and (df["Discount_Pct"] <= 40).all(), "Discount out of range [0, 40]"
    assert (df["Quantity"] >= 1).all(), "Quantity must be >= 1"
    valid_ratings = df["Customer_Rating"].dropna()
    assert (valid_ratings >= 1.0).all() and (valid_ratings <= 5.0).all(), "Rating out of range [1, 5]"

    # Recalculate Total_Amount check
    expected_amount = df["Unit_Price"] * df["Quantity"] * (1 - df["Discount_Pct"] / 100)
    diff = np.abs(df["Total_Amount"] - expected_amount)
    max_diff = diff.max()
    mismatch_cnt = (diff > 0.01).sum()
    print(f"      Total_Amount formula check: max discrepancy = {max_diff:.4f} INR ({mismatch_cnt} errors)")
    assert mismatch_cnt == 0, f"Found {mismatch_cnt} Total_Amount mismatches!"

    # Step 5: Derive analytics dimensions
    print("[6/7] Engineering derived analytics features...")
    df["Year"] = df["Order_Date"].dt.year
    df["Month"] = df["Order_Date"].dt.month
    df["Month_Name"] = df["Order_Date"].dt.strftime("%b")
    df["Quarter"] = "Q" + df["Order_Date"].dt.quarter.astype(str)
    df["Year_Month"] = df["Order_Date"].dt.strftime("%Y-%m")
    
    # Net Revenue flag: Delivered or Shipped only
    df["Net_Flag"] = df["Order_Status"].isin(["Delivered", "Shipped"])

    # Categorical bins
    df["Age_Group"] = df["Age"].apply(classify_age_group)
    df["Discount_Band"] = df["Discount_Pct"].apply(classify_discount_band)
    df["Is_Festive_Season"] = df["Order_Date"].apply(is_festive_season)

    # Step 6: Export processed outputs
    print("[7/7] Exporting cleaned datasets...")
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    df.to_parquet(CLEAN_PARQUET_PATH, index=False)
    print(f"      Saved Parquet: {CLEAN_PARQUET_PATH} ({CLEAN_PARQUET_PATH.stat().st_size / 1024:.1f} KB)")

    # Save Excel version
    with pd.ExcelWriter(CLEAN_EXCEL_PATH, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Clean_Orders_Data", index=False)
    print(f"      Saved Excel:   {CLEAN_EXCEL_PATH} ({CLEAN_EXCEL_PATH.stat().st_size / 1024:.1f} KB)")

    rows_out = len(df)
    print("=" * 60)
    print("CLEANSING SUMMARY:")
    print(f"  Rows in:            {rows_in:,}")
    print(f"  Duplicates removed: {dup_count:,}")
    print(f"  Final clean rows:   {rows_out:,}")
    print(f"  Unique Order IDs:   {df['Order_ID'].nunique():,}")
    print(f"  Unique Customers:   {df['Customer_ID'].nunique():,}")
    print("=" * 60)

    return df


if __name__ == "__main__":
    clean_ecommerce_data()
