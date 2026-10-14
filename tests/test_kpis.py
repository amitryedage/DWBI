"""Unit tests for KPI calculation functions.

Tests all 13 business KPIs against:
1. A deterministic synthetic test DataFrame with hand-calculated expected values.
2. Edge cases (empty DataFrame, zero denominators, unrated orders).
3. The real cleaned analytical dataset (cross-validation).
"""

import pytest
import pandas as pd
import numpy as np
from src.kpis import (
    compute_net_revenue,
    compute_total_orders,
    compute_unique_customers,
    compute_aov,
    compute_revenue_per_customer,
    compute_repeat_purchase_rate,
    compute_cancellation_rate,
    compute_return_rate,
    compute_avg_discount,
    compute_avg_delivery_days,
    compute_avg_rating,
    compute_mom_growth,
    compute_top_segment_share,
    compute_all_kpis,
)
from src.config import CLEAN_PARQUET_PATH


@pytest.fixture
def sample_orders_df():
    """Deterministic 4-order DataFrame with known values.
    
    Orders:
    - O1: Delivered, Cust_A, Seg: Loyal, Rs. 1,000, 10% disc, 3 days deliv, 5 rating, 2024-01-10
    - O2: Shipped,   Cust_A, Seg: Loyal, Rs. 2,000, 20% disc, NaN days deliv, NaN rating, 2024-01-15
    - O3: Cancelled, Cust_B, Seg: New,   Rs. 1,500,  0% disc, NaN days deliv, NaN rating, 2024-02-10
    - O4: Returned,  Cust_C, Seg: Regular, Rs. 500,  5% disc, 5 days deliv, 3 rating, 2024-02-15
    """
    data = {
        "Order_ID": ["O1", "O2", "O3", "O4"],
        "Customer_ID": ["Cust_A", "Cust_A", "Cust_B", "Cust_C"],
        "Customer_Segment": ["Loyal", "Loyal", "New", "Regular"],
        "Order_Status": ["Delivered", "Shipped", "Cancelled", "Returned"],
        "Total_Amount": [1000.0, 2000.0, 1500.0, 500.0],
        "Discount_Pct": [10.0, 20.0, 0.0, 5.0],
        "Delivery_Days": [3.0, np.nan, np.nan, 5.0],
        "Customer_Rating": [5.0, np.nan, np.nan, 3.0],
        "Order_Date": pd.to_datetime(["2024-01-10", "2024-01-15", "2024-02-10", "2024-02-15"]),
        "Year_Month": ["2024-01", "2024-01", "2024-02", "2024-02"],
        "Net_Flag": [True, True, False, False],
    }
    return pd.DataFrame(data)


def test_synthetic_kpis(sample_orders_df):
    """Verify exact hand-calculated KPI results on the sample DataFrame."""
    # 1. Net Revenue: O1 + O2 = 1000 + 2000 = 3000
    assert compute_net_revenue(sample_orders_df) == 3000.0
    
    # 2. Total Orders: 4
    assert compute_total_orders(sample_orders_df) == 4
    
    # 3. Unique Customers: Cust_A, Cust_B, Cust_C = 3
    assert compute_unique_customers(sample_orders_df) == 3
    
    # 4. AOV: Net Revenue (3000) / Net Orders (2) = 1500.0
    assert compute_aov(sample_orders_df) == 1500.0
    
    # 5. Rev per Customer: Net Revenue (3000) / 3 = 1000.0
    assert compute_revenue_per_customer(sample_orders_df) == 1000.0
    
    # 6. Repeat Purchase Rate: Cust_A has 2 orders, others have 1 -> 1 / 3 = 33.333%
    assert pytest.approx(compute_repeat_purchase_rate(sample_orders_df), 0.01) == 33.33
    
    # 7. Cancellation Rate: 1 / 4 = 25.0%
    assert compute_cancellation_rate(sample_orders_df) == 25.0
    
    # 8. Return Rate: 1 returned / (1 delivered + 1 returned) = 50.0%
    assert compute_return_rate(sample_orders_df) == 50.0
    
    # 9. Avg Discount: (10 + 20 + 0 + 5) / 4 = 8.75%
    assert compute_avg_discount(sample_orders_df) == 8.75
    
    # 10. Avg Delivery Days: (3 + 5) / 2 = 4.0 days
    assert compute_avg_delivery_days(sample_orders_df) == 4.0
    
    # 11. Avg Rating: (5 + 3) / 2 = 4.0
    assert compute_avg_rating(sample_orders_df) == 4.0
    
    # 12. Top Segment Share: Loyal has 3000 out of 3000 = 100.0%
    top_seg, share = compute_top_segment_share(sample_orders_df)
    assert top_seg == "Loyal"
    assert share == 100.0


def test_edge_cases_empty_dataframe():
    """Verify that empty DataFrames do not crash with ZeroDivisionError."""
    empty_df = pd.DataFrame(columns=[
        "Order_ID", "Customer_ID", "Customer_Segment", "Order_Status",
        "Total_Amount", "Discount_Pct", "Delivery_Days", "Customer_Rating",
        "Year_Month", "Net_Flag"
    ])
    assert compute_net_revenue(empty_df) == 0.0
    assert compute_total_orders(empty_df) == 0
    assert compute_unique_customers(empty_df) == 0
    assert compute_aov(empty_df) == 0.0
    assert compute_revenue_per_customer(empty_df) == 0.0
    assert compute_repeat_purchase_rate(empty_df) == 0.0
    assert compute_cancellation_rate(empty_df) == 0.0
    assert compute_return_rate(empty_df) == 0.0
    assert compute_avg_discount(empty_df) == 0.0
    assert compute_avg_delivery_days(empty_df) == 0.0
    assert compute_avg_rating(empty_df) == 0.0
    assert compute_mom_growth(empty_df) == 0.0
    assert compute_top_segment_share(empty_df) == ("None", 0.0)


def test_edge_case_zero_delivered():
    """When all orders are cancelled, AOV and Return Rate must return 0.0 gracefully."""
    data = {
        "Order_ID": ["O1", "O2"],
        "Customer_ID": ["C1", "C2"],
        "Customer_Segment": ["New", "New"],
        "Order_Status": ["Cancelled", "Cancelled"],
        "Total_Amount": [500.0, 700.0],
        "Discount_Pct": [0.0, 0.0],
        "Delivery_Days": [np.nan, np.nan],
        "Customer_Rating": [np.nan, np.nan],
        "Year_Month": ["2024-01", "2024-01"],
        "Net_Flag": [False, False],
    }
    df = pd.DataFrame(data)
    assert compute_net_revenue(df) == 0.0
    assert compute_aov(df) == 0.0
    assert compute_return_rate(df) == 0.0
    assert compute_cancellation_rate(df) == 100.0


def test_real_dataset_cross_validation():
    """Cross-validate 5 major KPIs on the real cleaned dataset."""
    assert CLEAN_PARQUET_PATH.exists()
    df = pd.read_parquet(CLEAN_PARQUET_PATH)

    # 1. Total Orders check
    assert compute_total_orders(df) == 9900

    # 2. Unique Customers check
    assert compute_unique_customers(df) == 2424

    # 3. Cancellation Rate check
    # 826 cancelled / 9900 total = ~8.34%
    cancel_cnt = (df["Order_Status"] == "Cancelled").sum()
    expected_cancel_rate = (cancel_cnt / 9900) * 100
    assert pytest.approx(compute_cancellation_rate(df), 0.001) == expected_cancel_rate

    # 4. Net Revenue check: Delivered + Shipped
    net_manual = df[df["Order_Status"].isin(["Delivered", "Shipped"])]["Total_Amount"].sum()
    assert pytest.approx(compute_net_revenue(df), 0.01) == net_manual

    # 5. Average Discount check
    disc_manual = df["Discount_Pct"].mean()
    assert pytest.approx(compute_avg_discount(df), 0.001) == disc_manual
