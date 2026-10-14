"""Plotly Visualization Module for E-Commerce Customer Analytics Dashboard.

Notice Phase 3 (V1 to V12 Visualizations):
Strictly adheres to the White/Light Background requirement:
- Plotly 'plotly_white' template
- Transparent / Pure white backgrounds
- Subtle gridlines (#E2E8F0)
- High-contrast dark typography (#0F172A, #1E293B)
- Cohesive, accessible color tokens
- Interactive hover tooltips & Indian Rupee (INR) formatting
"""

from typing import List
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from src.config import (
    PLOTLY_TEMPLATE,
    COLOR_BG,
    COLOR_SECONDARY_BG,
    COLOR_BORDER,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_PRIMARY_BLUE,
    STATUS_COLORS,
    SEGMENT_COLORS,
    CATEGORICAL_PALETTE,
    format_inr,
)

# Standard layout styling for consistent light theme
LIGHT_LAYOUT = dict(
    template=PLOTLY_TEMPLATE,
    paper_bgcolor="rgba(255, 255, 255, 0)",
    plot_bgcolor="rgba(255, 255, 255, 0)",
    margin=dict(l=40, r=30, t=50, b=40),
    font=dict(color=COLOR_TEXT_PRIMARY, family="sans-serif", size=12),
    hoverlabel=dict(
        bgcolor="#FFFFFF",
        bordercolor=COLOR_BORDER,
        font=dict(color=COLOR_TEXT_PRIMARY, size=12),
    ),
)


def empty_figure(title: str = "No Data Available") -> go.Figure:
    """Return a clean empty placeholder figure when filtered data is empty."""
    fig = go.Figure()
    fig.add_annotation(
        text=title,
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=14, color=COLOR_TEXT_SECONDARY),
    )
    fig.update_layout(**LIGHT_LAYOUT, xaxis=dict(visible=False), yaxis=dict(visible=False))
    return fig


# -----------------------------------------------------------------------------
# TAB 1: OVERVIEW CHARTS
# -----------------------------------------------------------------------------

def chart_monthly_revenue(df: pd.DataFrame) -> go.Figure:
    """V1: Monthly Net Revenue Trend Line with Festive Peaks."""
    if df.empty:
        return empty_figure("No transactions matching filters")

    net_df = df[df["Net_Flag"] == True].copy()
    if net_df.empty:
        return empty_figure("No delivered/shipped orders in selection")

    monthly = (
        net_df.groupby("Year_Month")
        .agg(
            Net_Revenue=("Total_Amount", "sum"),
            Orders=("Order_ID", "nunique"),
            Festive_Share=("Is_Festive_Season", "mean"),
        )
        .reset_index()
    )

    fig = go.Figure()

    # Base revenue line
    fig.add_trace(
        go.Scatter(
            x=monthly["Year_Month"],
            y=monthly["Net_Revenue"],
            mode="lines+markers",
            name="Net Revenue",
            line=dict(color=COLOR_PRIMARY_BLUE, width=3),
            marker=dict(size=7, color=COLOR_PRIMARY_BLUE),
            hovertemplate="<b>%{x}</b><br>Net Revenue: ₹%{y:,.0f}<extra></extra>",
        )
    )

    # Highlight festive months (Oct/Nov of each year)
    festive_months = monthly[monthly["Year_Month"].isin(["2024-10", "2024-11", "2025-10", "2025-11"])]
    if not festive_months.empty:
        fig.add_trace(
            go.Scatter(
                x=festive_months["Year_Month"],
                y=festive_months["Net_Revenue"],
                mode="markers",
                name="Festive Season",
                marker=dict(size=12, color="#E11D48", symbol="diamond"),
                hovertemplate="<b>%{x} (Festive Peak)</b><br>Net Revenue: ₹%{y:,.0f}<extra></extra>",
            )
        )

    fig.update_layout(
        **LIGHT_LAYOUT,
        title="<b>V1: Monthly Net Revenue Trend (2024 - 2025)</b>",
        xaxis=dict(title="Month", tickangle=-45, showgrid=True, gridcolor=COLOR_BORDER),
        yaxis=dict(title="Net Revenue (INR)", showgrid=True, gridcolor=COLOR_BORDER),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def chart_category_revenue(df: pd.DataFrame) -> go.Figure:
    """V3: Net Revenue by Product Category (Horizontal Bar)."""
    if df.empty:
        return empty_figure("No category data available")

    net_df = df[df["Net_Flag"] == True]
    if net_df.empty:
        return empty_figure("No delivered/shipped orders")

    cat_data = (
        net_df.groupby("Product_Category")["Total_Amount"]
        .sum()
        .reset_index()
        .sort_values("Total_Amount", ascending=True)
    )

    fig = px.bar(
        cat_data,
        x="Total_Amount",
        y="Product_Category",
        orientation="h",
        color="Product_Category",
        color_discrete_sequence=CATEGORICAL_PALETTE,
        text=cat_data["Total_Amount"].apply(lambda x: format_inr(x)),
    )
    fig.update_traces(
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Revenue: ₹%{x:,.0f}<extra></extra>",
    )
    fig.update_layout(
        **LIGHT_LAYOUT,
        showlegend=False,
        title="<b>V3: Net Revenue by Product Category</b>",
        xaxis=dict(title="Net Revenue (INR)", showgrid=True, gridcolor=COLOR_BORDER),
        yaxis=dict(title="", showgrid=False),
    )
    return fig


def chart_order_status_share(df: pd.DataFrame) -> go.Figure:
    """V7: Order Status Share (Donut Chart)."""
    if df.empty:
        return empty_figure("No order status data")

    status_data = df["Order_Status"].value_counts().reset_index()
    status_data.columns = ["Order_Status", "Count"]

    color_map = [STATUS_COLORS.get(s, "#94A3B8") for s in status_data["Order_Status"]]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=status_data["Order_Status"],
                values=status_data["Count"],
                hole=0.45,
                marker=dict(colors=color_map, line=dict(color="#FFFFFF", width=2)),
                textinfo="label+percent",
                hovertemplate="<b>%{label}</b><br>Orders: %{value:,} (%{percent})<extra></extra>",
            )
        ]
    )
    fig.update_layout(
        **LIGHT_LAYOUT,
        title="<b>V7: Order Status Fulfillment Breakdown</b>",
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
    )
    return fig


# -----------------------------------------------------------------------------
# TAB 2: CUSTOMERS CHARTS
# -----------------------------------------------------------------------------

def chart_segment_revenue(df: pd.DataFrame) -> go.Figure:
    """V4: Net Revenue by Customer Segment (Bar Chart)."""
    if df.empty:
        return empty_figure("No segment data")

    net_df = df[df["Net_Flag"] == True]
    if net_df.empty:
        return empty_figure("No delivered/shipped orders")

    seg_data = (
        net_df.groupby("Customer_Segment")["Total_Amount"]
        .sum()
        .reset_index()
        .sort_values("Total_Amount", ascending=False)
    )

    color_map = [SEGMENT_COLORS.get(s, COLOR_PRIMARY_BLUE) for s in seg_data["Customer_Segment"]]

    fig = px.bar(
        seg_data,
        x="Customer_Segment",
        y="Total_Amount",
        color="Customer_Segment",
        color_discrete_map=SEGMENT_COLORS,
        text=seg_data["Total_Amount"].apply(lambda x: format_inr(x)),
    )
    fig.update_traces(
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Net Revenue: ₹%{y:,.0f}<extra></extra>",
    )
    fig.update_layout(
        **LIGHT_LAYOUT,
        showlegend=False,
        title="<b>V4: Net Revenue by Customer Segment</b>",
        xaxis=dict(title="Segment", showgrid=False),
        yaxis=dict(title="Net Revenue (INR)", showgrid=True, gridcolor=COLOR_BORDER),
    )
    return fig


def chart_segment_customer_mix(df: pd.DataFrame) -> go.Figure:
    """V9: Customer Count by Segment (Donut Chart)."""
    if df.empty:
        return empty_figure("No customer data")

    cust_mix = df.groupby("Customer_Segment")["Customer_ID"].nunique().reset_index()
    cust_mix.columns = ["Customer_Segment", "Unique_Customers"]

    color_map = [SEGMENT_COLORS.get(s, COLOR_PRIMARY_BLUE) for s in cust_mix["Customer_Segment"]]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=cust_mix["Customer_Segment"],
                values=cust_mix["Unique_Customers"],
                hole=0.45,
                marker=dict(colors=color_map, line=dict(color="#FFFFFF", width=2)),
                textinfo="label+percent",
                hovertemplate="<b>%{label}</b><br>Customers: %{value:,} (%{percent})<extra></extra>",
            )
        ]
    )
    fig.update_layout(
        **LIGHT_LAYOUT,
        title="<b>V9: Customer Base Mix by Segment</b>",
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
    )
    return fig


def chart_age_group_revenue(df: pd.DataFrame) -> go.Figure:
    """V12: Net Revenue by Age Group (Bar Chart)."""
    if df.empty:
        return empty_figure("No age data")

    net_df = df[df["Net_Flag"] == True]
    if net_df.empty:
        return empty_figure("No delivered/shipped orders")

    order_seq = ["<25", "25-34", "35-49", "50+"]
    age_data = (
        net_df.groupby("Age_Group")["Total_Amount"]
        .sum()
        .reindex(order_seq)
        .dropna()
        .reset_index()
    )

    fig = px.bar(
        age_data,
        x="Age_Group",
        y="Total_Amount",
        color="Age_Group",
        color_discrete_sequence=["#3B82F6", "#2563EB", "#1D4ED8", "#1E40AF"],
        text=age_data["Total_Amount"].apply(lambda x: format_inr(x)),
    )
    fig.update_traces(
        textposition="outside",
        hovertemplate="<b>Age Group: %{x}</b><br>Revenue: ₹%{y:,.0f}<extra></extra>",
    )
    fig.update_layout(
        **LIGHT_LAYOUT,
        showlegend=False,
        title="<b>V12: Net Revenue by Demographic Age Group</b>",
        xaxis=dict(title="Age Cohort", showgrid=False),
        yaxis=dict(title="Net Revenue (INR)", showgrid=True, gridcolor=COLOR_BORDER),
    )
    return fig


def chart_repeat_vs_onetime(df: pd.DataFrame) -> go.Figure:
    """Repeat vs One-Time Buyers Share (Donut Chart)."""
    if df.empty:
        return empty_figure("No order data")

    order_counts = df.groupby("Customer_ID")["Order_ID"].nunique()
    repeat_count = (order_counts >= 2).sum()
    onetime_count = (order_counts == 1).sum()

    labels = ["Repeat Buyers (≥2 orders)", "One-Time Buyers (1 order)"]
    values = [repeat_count, onetime_count]
    colors = ["#10B981", "#94A3B8"]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.45,
                marker=dict(colors=colors, line=dict(color="#FFFFFF", width=2)),
                textinfo="label+percent",
                hovertemplate="<b>%{label}</b><br>Customers: %{value:,} (%{percent})<extra></extra>",
            )
        ]
    )
    fig.update_layout(
        **LIGHT_LAYOUT,
        title="<b>Customer Retention: Repeat vs One-Time Buyers</b>",
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
    )
    return fig


# -----------------------------------------------------------------------------
# TAB 3: PRODUCTS CHARTS
# -----------------------------------------------------------------------------

def chart_top_products(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """V6: Top 10 Products by Net Revenue (Horizontal Bar)."""
    if df.empty:
        return empty_figure("No product data")

    net_df = df[df["Net_Flag"] == True]
    if net_df.empty:
        return empty_figure("No delivered/shipped orders")

    prod_data = (
        net_df.groupby(["Product_Name", "Product_Category"])["Total_Amount"]
        .sum()
        .reset_index()
        .sort_values("Total_Amount", ascending=True)
        .tail(top_n)
    )

    fig = px.bar(
        prod_data,
        x="Total_Amount",
        y="Product_Name",
        color="Product_Category",
        orientation="h",
        color_discrete_sequence=CATEGORICAL_PALETTE,
        text=prod_data["Total_Amount"].apply(lambda x: format_inr(x)),
    )
    fig.update_traces(
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Category: %{customdata[0]}<br>Revenue: ₹%{x:,.0f}<extra></extra>",
        customdata=prod_data[["Product_Category"]],
    )
    fig.update_layout(
        **LIGHT_LAYOUT,
        title=f"<b>V6: Top {top_n} Revenue-Generating Products</b>",
        xaxis=dict(title="Net Revenue (INR)", showgrid=True, gridcolor=COLOR_BORDER),
        yaxis=dict(title="", showgrid=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def chart_category_revenue_pie(df: pd.DataFrame) -> go.Figure:
    """Category Revenue Share (Pie / Donut Chart)."""
    if df.empty:
        return empty_figure("No category data")

    net_df = df[df["Net_Flag"] == True]
    if net_df.empty:
        return empty_figure("No delivered/shipped orders")

    cat_data = (
        net_df.groupby("Product_Category")["Total_Amount"]
        .sum()
        .reset_index()
        .sort_values("Total_Amount", ascending=False)
    )

    # Group into top 5 + Other
    if len(cat_data) > 6:
        top_5 = cat_data.iloc[:5]
        other_sum = cat_data.iloc[5:]["Total_Amount"].sum()
        other_df = pd.DataFrame([{"Product_Category": "Other Categories", "Total_Amount": other_sum}])
        cat_data = pd.concat([top_5, other_df], ignore_index=True)

    fig = go.Figure(
        data=[
            go.Pie(
                labels=cat_data["Product_Category"],
                values=cat_data["Total_Amount"],
                hole=0.45,
                marker=dict(colors=CATEGORICAL_PALETTE, line=dict(color="#FFFFFF", width=2)),
                textinfo="label+percent",
                hovertemplate="<b>%{label}</b><br>Revenue: ₹%{value:,.0f} (%{percent})<extra></extra>",
            )
        ]
    )
    fig.update_layout(
        **LIGHT_LAYOUT,
        title="<b>Category Contribution to Net Revenue</b>",
        legend=dict(orientation="h", yanchor="bottom", y=-0.18, xanchor="center", x=0.5),
    )
    return fig


def chart_discount_vs_aov(df: pd.DataFrame) -> go.Figure:
    """V10: Discount Band vs Average Order Value (Bar Chart)."""
    if df.empty:
        return empty_figure("No discount data")

    net_df = df[df["Net_Flag"] == True]
    if net_df.empty:
        return empty_figure("No delivered/shipped orders")

    band_order = ["No Discount (0%)", "Low (1-10%)", "Medium (11-20%)", "High (21-30%)", "Very High (>30%)"]
    disc_data = (
        net_df.groupby("Discount_Band")
        .agg(
            AOV=("Total_Amount", "mean"),
            Orders=("Order_ID", "count"),
        )
        .reindex(band_order)
        .dropna()
        .reset_index()
    )

    fig = px.bar(
        disc_data,
        x="Discount_Band",
        y="AOV",
        color="Discount_Band",
        color_discrete_sequence=["#10B981", "#3B82F6", "#F59E0B", "#EA580C", "#EF4444"],
        text=disc_data["AOV"].apply(lambda x: format_inr(x, compact=False)),
    )
    fig.update_traces(
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Average Order Value: ₹%{y:,.2f}<br>Order Count: %{customdata[0]:,}<extra></extra>",
        customdata=disc_data[["Orders"]],
    )
    fig.update_layout(
        **LIGHT_LAYOUT,
        showlegend=False,
        title="<b>V10: Average Order Value (AOV) by Discount Band</b>",
        xaxis=dict(title="Promotional Discount Band", showgrid=False),
        yaxis=dict(title="AOV (INR)", showgrid=True, gridcolor=COLOR_BORDER),
    )
    return fig


def chart_category_monthly_trend(df: pd.DataFrame) -> go.Figure:
    """V2: Multi-line Category Revenue Monthly Trend."""
    if df.empty:
        return empty_figure("No monthly category data")

    net_df = df[df["Net_Flag"] == True]
    if net_df.empty:
        return empty_figure("No delivered/shipped orders")

    cat_monthly = (
        net_df.groupby(["Year_Month", "Product_Category"])["Total_Amount"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        cat_monthly,
        x="Year_Month",
        y="Total_Amount",
        color="Product_Category",
        color_discrete_sequence=CATEGORICAL_PALETTE,
        markers=True,
    )
    fig.update_traces(
        line=dict(width=2.5),
        marker=dict(size=5),
        hovertemplate="<b>%{x}</b><br>%{data.name}: ₹%{y:,.0f}<extra></extra>",
    )
    fig.update_layout(
        **LIGHT_LAYOUT,
        title="<b>V2: Category Revenue Trend (Multi-Line)</b>",
        xaxis=dict(title="Month", tickangle=-45, showgrid=True, gridcolor=COLOR_BORDER),
        yaxis=dict(title="Net Revenue (INR)", showgrid=True, gridcolor=COLOR_BORDER),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


# -----------------------------------------------------------------------------
# TAB 4: OPERATIONS CHARTS
# -----------------------------------------------------------------------------

def chart_operational_rates(df: pd.DataFrame) -> go.Figure:
    """V11: Monthly Cancellation & Return Rate Trends (Line Chart)."""
    if df.empty:
        return empty_figure("No operational data")

    monthly_ops = []
    for ym, group in df.groupby("Year_Month"):
        tot = len(group)
        cancelled = (group["Order_Status"] == "Cancelled").sum()
        c_rate = (cancelled / tot * 100) if tot > 0 else 0
        
        delivered = (group["Order_Status"] == "Delivered").sum()
        returned = (group["Order_Status"] == "Returned").sum()
        denom = delivered + returned
        r_rate = (returned / denom * 100) if denom > 0 else 0
        
        monthly_ops.append({
            "Year_Month": ym,
            "Cancellation_Rate": c_rate,
            "Return_Rate": r_rate,
        })

    ops_df = pd.DataFrame(monthly_ops).sort_values("Year_Month")

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=ops_df["Year_Month"],
            y=ops_df["Cancellation_Rate"],
            mode="lines+markers",
            name="Cancellation Rate (%)",
            line=dict(color="#EF4444", width=2.5),
            marker=dict(size=6),
            hovertemplate="<b>%{x}</b><br>Cancellation Rate: %{y:.2f}%<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=ops_df["Year_Month"],
            y=ops_df["Return_Rate"],
            mode="lines+markers",
            name="Return Rate (%)",
            line=dict(color="#F59E0B", width=2.5),
            marker=dict(size=6),
            hovertemplate="<b>%{x}</b><br>Return Rate: %{y:.2f}%<extra></extra>",
        )
    )
    fig.update_layout(
        **LIGHT_LAYOUT,
        title="<b>V11: Monthly Cancellation vs. Return Rates</b>",
        xaxis=dict(title="Month", tickangle=-45, showgrid=True, gridcolor=COLOR_BORDER),
        yaxis=dict(title="Rate (%)", showgrid=True, gridcolor=COLOR_BORDER),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def chart_payment_methods(df: pd.DataFrame) -> go.Figure:
    """V8: Payment Method Share (Donut Chart)."""
    if df.empty:
        return empty_figure("No payment data")

    pm_data = df["Payment_Method"].value_counts().reset_index()
    pm_data.columns = ["Payment_Method", "Orders"]

    # Group into top 5 + Other
    if len(pm_data) > 6:
        top_5 = pm_data.iloc[:5]
        other_sum = pm_data.iloc[5:]["Orders"].sum()
        other_df = pd.DataFrame([{"Payment_Method": "Other Methods", "Orders": other_sum}])
        pm_data = pd.concat([top_5, other_df], ignore_index=True)

    fig = go.Figure(
        data=[
            go.Pie(
                labels=pm_data["Payment_Method"],
                values=pm_data["Orders"],
                hole=0.45,
                marker=dict(colors=CATEGORICAL_PALETTE, line=dict(color="#FFFFFF", width=2)),
                textinfo="label+percent",
                hovertemplate="<b>%{label}</b><br>Orders: %{value:,} (%{percent})<extra></extra>",
            )
        ]
    )
    fig.update_layout(
        **LIGHT_LAYOUT,
        title="<b>V8: Customer Payment Method Mix</b>",
        legend=dict(orientation="h", yanchor="bottom", y=-0.18, xanchor="center", x=0.5),
    )
    return fig


def chart_device_types(df: pd.DataFrame) -> go.Figure:
    """Device Type Distribution (Bar Chart)."""
    if df.empty:
        return empty_figure("No device data")

    dev_data = df["Device_Type"].value_counts().reset_index()
    dev_data.columns = ["Device_Type", "Orders"]

    fig = px.bar(
        dev_data,
        x="Device_Type",
        y="Orders",
        color="Device_Type",
        color_discrete_sequence=["#2563EB", "#0D9488", "#7C3AED", "#EA580C"],
        text=dev_data["Orders"].apply(lambda x: f"{x:,}"),
    )
    fig.update_traces(
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Orders: %{y:,}<extra></extra>",
    )
    fig.update_layout(
        **LIGHT_LAYOUT,
        showlegend=False,
        title="<b>Orders by User Device Channel</b>",
        xaxis=dict(title="Device", showgrid=False),
        yaxis=dict(title="Orders Count", showgrid=True, gridcolor=COLOR_BORDER),
    )
    return fig


def chart_delivery_by_state(df: pd.DataFrame) -> go.Figure:
    """Average Delivery Days by State (Top 10 States)."""
    if df.empty:
        return empty_figure("No logistics data")

    deliv_df = df[df["Order_Status"].isin(["Delivered", "Returned"])].dropna(subset=["Delivery_Days"])
    if deliv_df.empty:
        return empty_figure("No completed delivery records")

    state_data = (
        deliv_df.groupby("State")["Delivery_Days"]
        .agg(["mean", "count"])
        .reset_index()
        .sort_values("mean", ascending=True)
        .head(10)
    )

    fig = px.bar(
        state_data,
        x="mean",
        y="State",
        orientation="h",
        color="mean",
        color_continuous_scale="Blues",
        text=state_data["mean"].apply(lambda x: f"{x:.1f}d"),
    )
    fig.update_traces(
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Avg Delivery: %{x:.2f} days<extra></extra>",
    )
    fig.update_layout(
        **LIGHT_LAYOUT,
        coloraxis_showscale=False,
        title="<b>Fulfillment Speed: Top 10 Fastest Delivery States</b>",
        xaxis=dict(title="Average Delivery Duration (Days)", showgrid=True, gridcolor=COLOR_BORDER),
        yaxis=dict(title="", showgrid=False),
    )
    return fig


def chart_rating_vs_delivery(df: pd.DataFrame) -> go.Figure:
    """Average Rating grouped by Delivery Days."""
    if df.empty:
        return empty_figure("No feedback data")

    reviewed = df.dropna(subset=["Customer_Rating", "Delivery_Days"])
    if reviewed.empty:
        return empty_figure("No reviewed deliveries")

    # Group delivery days into buckets: <=2 days, 3-4 days, 5-6 days, 7+ days
    def bucket_days(d):
        if d <= 2:
            return "Fast (≤2 days)"
        elif d <= 4:
            return "Standard (3-4 days)"
        elif d <= 6:
            return "Moderate (5-6 days)"
        else:
            return "Slow (≥7 days)"

    reviewed = reviewed.copy()
    reviewed["Speed_Bucket"] = reviewed["Delivery_Days"].apply(bucket_days)
    
    bucket_order = ["Fast (≤2 days)", "Standard (3-4 days)", "Moderate (5-6 days)", "Slow (≥7 days)"]
    grouped = (
        reviewed.groupby("Speed_Bucket")["Customer_Rating"]
        .agg(["mean", "count"])
        .reindex(bucket_order)
        .dropna()
        .reset_index()
    )

    fig = px.bar(
        grouped,
        x="Speed_Bucket",
        y="mean",
        color="Speed_Bucket",
        color_discrete_sequence=["#10B981", "#3B82F6", "#F59E0B", "#EF4444"],
        text=grouped["mean"].apply(lambda x: f"{x:.2f} ★"),
    )
    fig.update_traces(
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Avg Rating: %{y:.2f} Stars<br>Reviews: %{customdata[0]:,}<extra></extra>",
        customdata=grouped[["count"]],
    )
    fig.update_layout(
        **LIGHT_LAYOUT,
        showlegend=False,
        title="<b>Customer Satisfaction vs Delivery Speed</b>",
        xaxis=dict(title="Fulfillment Turnaround", showgrid=False),
        yaxis=dict(title="Average Star Rating", range=[1, 5.3], showgrid=True, gridcolor=COLOR_BORDER),
    )
    return fig
