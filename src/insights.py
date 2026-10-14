"""Dynamic Business Insights Generator for E-Commerce Customer Analytics Dashboard.

Produces data-driven, executive bullet points with dynamic real numbers:
- Festive season uplift
- Dominant product categories
- VIP & Loyal segment revenue contribution
- Payment method friction & cancellation correlation
- Delivery turnaround speed impact on customer rating
"""

from typing import List
import pandas as pd
from src.config import format_inr, format_percent


def generate_executive_insights(df: pd.DataFrame) -> List[str]:
    """Analyze current filtered DataFrame and return dynamic business findings."""
    if df.empty:
        return ["No transactions match current filters. Reset filters to view executive insights."]

    insights = []
    net_df = df[df["Net_Flag"] == True]
    total_net = net_df["Total_Amount"].sum()

    # Insight 1: Top Product Category Share
    if not net_df.empty:
        cat_rev = net_df.groupby("Product_Category")["Total_Amount"].sum()
        top_cat = cat_rev.idxmax()
        top_cat_share = (cat_rev.max() / total_net) * 100
        insights.append(
            f"**Top Category Performance:** **{top_cat}** leads sales, contributing **{format_inr(cat_rev.max())}** "
            f"({top_cat_share:.1f}% of total net revenue). Prioritize marketing spend and inventory depth here."
        )

    # Insight 2: Festive Season Peak Impact
    if "Is_Festive_Season" in net_df.columns and net_df["Is_Festive_Season"].nunique() > 1:
        festive_df = net_df[net_df["Is_Festive_Season"] == True]
        non_festive_df = net_df[net_df["Is_Festive_Season"] == False]
        if not festive_df.empty and not non_festive_df.empty:
            festive_daily = festive_df["Total_Amount"].sum() / max(1, festive_df["Order_Date"].nunique())
            regular_daily = non_festive_df["Total_Amount"].sum() / max(1, non_festive_df["Order_Date"].nunique())
            if regular_daily > 0:
                uplift = ((festive_daily - regular_daily) / regular_daily) * 100
                insights.append(
                    f"**Festive Season Surge:** Daily demand surges by **+{uplift:.1f}%** during festive periods "
                    f"(mid-Oct to mid-Nov) compared to regular trading periods."
                )

    # Insight 3: Customer Segment Concentration
    if not net_df.empty:
        seg_rev = net_df.groupby("Customer_Segment")["Total_Amount"].sum()
        loyal_vip_rev = seg_rev.get("Loyal", 0) + seg_rev.get("VIP", 0)
        loyal_vip_share = (loyal_vip_rev / total_net) * 100 if total_net > 0 else 0
        
        all_cust = df.groupby("Customer_Segment")["Customer_ID"].nunique()
        loyal_vip_cust = all_cust.get("Loyal", 0) + all_cust.get("VIP", 0)
        tot_cust = all_cust.sum()
        loyal_vip_cust_share = (loyal_vip_cust / tot_cust) * 100 if tot_cust > 0 else 0
        
        insights.append(
            f"**High-Value Retention:** **Loyal & VIP** buyers constitute **{loyal_vip_cust_share:.1f}%** of shoppers "
            f"but generate **{loyal_vip_share:.1f}%** of total net revenue ({format_inr(loyal_vip_rev)})."
        )

    # Insight 4: Operational Friction & COD Cancellations
    tot_orders = len(df)
    cancelled = (df["Order_Status"] == "Cancelled").sum()
    c_rate = (cancelled / tot_orders) * 100 if tot_orders > 0 else 0
    
    cod_orders = df[df["Payment_Method"] == "Cash on Delivery"]
    if not cod_orders.empty:
        cod_cancel = (cod_orders["Order_Status"] == "Cancelled").sum()
        cod_c_rate = (cod_cancel / len(cod_orders)) * 100
        insights.append(
            f"**Fulfillment Risk:** Platform cancellation rate is **{c_rate:.1f}%**. Orders placed via "
            f"**Cash on Delivery (COD)** suffer a higher cancellation rate of **{cod_c_rate:.1f}%**. "
            f"Incentivizing prepaid UPI can reduce RTO (Return to Origin) losses."
        )
    else:
        insights.append(f"**Operational Quality:** Overall order cancellation rate stands at **{c_rate:.1f}%**.")

    # Insight 5: Logistics Speed & Customer Satisfaction Link
    deliv_df = df.dropna(subset=["Delivery_Days", "Customer_Rating"])
    if not deliv_df.empty:
        fast_orders = deliv_df[deliv_df["Delivery_Days"] <= 2]
        slow_orders = deliv_df[deliv_df["Delivery_Days"] >= 6]
        fast_rating = fast_orders["Customer_Rating"].mean() if not fast_orders.empty else None
        slow_rating = slow_orders["Customer_Rating"].mean() if not slow_orders.empty else None
        
        if fast_rating and slow_rating:
            insights.append(
                f"**Logistics CSAT Correlation:** Orders delivered within **≤2 days** score **{fast_rating:.2f} ★**, "
                f"compared to **{slow_rating:.2f} ★** for deliveries taking **≥6 days**. Expedited shipping directly elevates customer sentiment."
            )
        else:
            avg_rt = deliv_df["Customer_Rating"].mean()
            insights.append(f"**Customer Sentiment:** Fulfilled orders maintain an average rating of **{avg_rt:.2f} / 5.0 ★**.")

    return insights
