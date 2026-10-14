"""KPI Calculation Functions for E-Commerce Customer Analytics Dashboard.

Notice Phase 1 & 3:
Implements all 13 core business KPIs with mathematical rigor,
edge-case safety (empty selections, zero denominators, null handling),
and formatted Indian Rupee (INR) presentation.
"""

from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np
from src.config import format_inr, format_percent


def compute_net_revenue(df: pd.DataFrame) -> float:
    """Sum of Total_Amount where status is Delivered or Shipped."""
    if df.empty:
        return 0.0
    net_orders = df[df["Net_Flag"] == True]
    return float(net_orders["Total_Amount"].sum())


def compute_total_orders(df: pd.DataFrame) -> int:
    """Count of unique Order_IDs."""
    if df.empty:
        return 0
    return int(df["Order_ID"].nunique())


def compute_unique_customers(df: pd.DataFrame) -> int:
    """Count of unique Customer_IDs."""
    if df.empty:
        return 0
    return int(df["Customer_ID"].nunique())


def compute_aov(df: pd.DataFrame) -> float:
    """Average Order Value: Net Revenue / Net Orders."""
    if df.empty:
        return 0.0
    net_df = df[df["Net_Flag"] == True]
    net_orders_count = net_df["Order_ID"].nunique()
    if net_orders_count == 0:
        return 0.0
    return float(net_df["Total_Amount"].sum() / net_orders_count)


def compute_revenue_per_customer(df: pd.DataFrame) -> float:
    """Net Revenue / Unique Customers."""
    if df.empty:
        return 0.0
    cust_count = compute_unique_customers(df)
    if cust_count == 0:
        return 0.0
    return float(compute_net_revenue(df) / cust_count)


def compute_repeat_purchase_rate(df: pd.DataFrame) -> float:
    """Percentage of customers with 2 or more orders."""
    if df.empty:
        return 0.0
    cust_counts = df.groupby("Customer_ID")["Order_ID"].nunique()
    total_cust = len(cust_counts)
    if total_cust == 0:
        return 0.0
    repeat_cust = (cust_counts >= 2).sum()
    return float((repeat_cust / total_cust) * 100.0)


def compute_cancellation_rate(df: pd.DataFrame) -> float:
    """Percentage of orders cancelled."""
    if df.empty:
        return 0.0
    total = len(df)
    if total == 0:
        return 0.0
    cancelled = (df["Order_Status"] == "Cancelled").sum()
    return float((cancelled / total) * 100.0)


def compute_return_rate(df: pd.DataFrame) -> float:
    """Returned orders / (Delivered + Returned orders)."""
    if df.empty:
        return 0.0
    returned = (df["Order_Status"] == "Returned").sum()
    delivered = (df["Order_Status"] == "Delivered").sum()
    denominator = returned + delivered
    if denominator == 0:
        return 0.0
    return float((returned / denominator) * 100.0)


def compute_avg_discount(df: pd.DataFrame) -> float:
    """Mean discount percentage."""
    if df.empty:
        return 0.0
    return float(df["Discount_Pct"].mean())


def compute_avg_delivery_days(df: pd.DataFrame) -> float:
    """Mean delivery duration in days for delivered/returned orders."""
    if df.empty:
        return 0.0
    delivered_or_returned = df[df["Order_Status"].isin(["Delivered", "Returned"])]
    valid_days = delivered_or_returned["Delivery_Days"].dropna()
    if valid_days.empty:
        return 0.0
    return float(valid_days.mean())


def compute_avg_rating(df: pd.DataFrame) -> float:
    """Mean rating for reviewed orders (excluding nulls)."""
    if df.empty:
        return 0.0
    valid_ratings = df["Customer_Rating"].dropna()
    if valid_ratings.empty:
        return 0.0
    return float(valid_ratings.mean())


def compute_mom_growth(df: pd.DataFrame) -> float:
    """Month-over-Month Net Revenue growth for the latest 2 available months."""
    if df.empty:
        return 0.0
    net_df = df[df["Net_Flag"] == True].copy()
    if net_df.empty:
        return 0.0
    
    monthly = net_df.groupby("Year_Month")["Total_Amount"].sum().sort_index()
    if len(monthly) < 2:
        return 0.0
    
    prev_rev = monthly.iloc[-2]
    curr_rev = monthly.iloc[-1]
    
    if prev_rev == 0:
        return 0.0
    return float(((curr_rev - prev_rev) / prev_rev) * 100.0)


def compute_top_segment_share(df: pd.DataFrame) -> Tuple[str, float]:
    """Top customer segment by Net Revenue and its share of total Net Revenue."""
    if df.empty:
        return ("None", 0.0)
    net_df = df[df["Net_Flag"] == True]
    if net_df.empty:
        return ("None", 0.0)
    
    seg_rev = net_df.groupby("Customer_Segment")["Total_Amount"].sum()
    total_net = seg_rev.sum()
    if total_net == 0:
        return ("None", 0.0)
    
    top_seg = seg_rev.idxmax()
    top_share = float((seg_rev.max() / total_net) * 100.0)
    return (str(top_seg), top_share)


def compute_all_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """Compute and format all 13 KPIs for dashboard presentation."""
    net_revenue = compute_net_revenue(df)
    total_orders = compute_total_orders(df)
    unique_cust = compute_unique_customers(df)
    aov = compute_aov(df)
    rev_per_cust = compute_revenue_per_customer(df)
    repeat_rate = compute_repeat_purchase_rate(df)
    cancel_rate = compute_cancellation_rate(df)
    return_rate = compute_return_rate(df)
    avg_discount = compute_avg_discount(df)
    avg_delivery = compute_avg_delivery_days(df)
    avg_rating = compute_avg_rating(df)
    mom_growth = compute_mom_growth(df)
    top_seg_name, top_seg_pct = compute_top_segment_share(df)

    return {
        # Raw numerical values
        "net_revenue_raw": net_revenue,
        "total_orders_raw": total_orders,
        "unique_cust_raw": unique_cust,
        "aov_raw": aov,
        "rev_per_cust_raw": rev_per_cust,
        "repeat_rate_raw": repeat_rate,
        "cancel_rate_raw": cancel_rate,
        "return_rate_raw": return_rate,
        "avg_discount_raw": avg_discount,
        "avg_delivery_raw": avg_delivery,
        "avg_rating_raw": avg_rating,
        "mom_growth_raw": mom_growth,
        "top_seg_name": top_seg_name,
        "top_seg_pct": top_seg_pct,
        
        # Formatted presentation strings
        "net_revenue_fmt": format_inr(net_revenue),
        "total_orders_fmt": f"{total_orders:,}",
        "unique_cust_fmt": f"{unique_cust:,}",
        "aov_fmt": format_inr(aov, compact=False),
        "rev_per_cust_fmt": format_inr(rev_per_cust, compact=False),
        "repeat_rate_fmt": format_percent(repeat_rate),
        "cancel_rate_fmt": format_percent(cancel_rate),
        "return_rate_fmt": format_percent(return_rate),
        "avg_discount_fmt": format_percent(avg_discount),
        "avg_delivery_fmt": f"{avg_delivery:.1f} days" if avg_delivery > 0 else "N/A",
        "avg_rating_fmt": f"{avg_rating:.2f} / 5.0" if avg_rating > 0 else "N/A",
        "mom_growth_fmt": f"{'+' if mom_growth > 0 else ''}{mom_growth:.1f}%",
        "top_seg_fmt": f"{top_seg_name} ({top_seg_pct:.1f}%)",
    }
