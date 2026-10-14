"""Interactive E-Commerce Customer Analytics Dashboard.

Course: Data Warehousing & Business Intelligence [1ADPE404]
Roll No: 4010 | Dept. of AI & Data Science, ADCET Ashta
Tech Stack: Streamlit + Plotly + pandas
Design: Strict Pure White & Light Theme (P0 Priority)
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path

# Local imports
from src.config import (
    CLEAN_PARQUET_PATH,
    CLEAN_EXCEL_PATH,
    RAW_DATA_PATH,
    format_inr,
    format_percent,
)
from src.kpis import compute_all_kpis
from src.charts import (
    chart_monthly_revenue,
    chart_category_revenue,
    chart_order_status_share,
    chart_segment_revenue,
    chart_segment_customer_mix,
    chart_age_group_revenue,
    chart_repeat_vs_onetime,
    chart_top_products,
    chart_category_revenue_pie,
    chart_discount_vs_aov,
    chart_category_monthly_trend,
    chart_operational_rates,
    chart_payment_methods,
    chart_device_types,
    chart_delivery_by_state,
    chart_rating_vs_delivery,
)
from src.insights import generate_executive_insights

# -----------------------------------------------------------------------------
# 1. STREAMLIT PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="E-Commerce Customer Analytics Dashboard | Roll 4010",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# 2. CUSTOM CSS: ENFORCE CLEAN WHITE / LIGHT THEME
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Global Background and Canvas */
    .stApp {
        background-color: #FFFFFF;
        color: #0F172A;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Top Header Bar */
    .header-container {
        background-color: #F8F9FA;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px 24px;
        margin-bottom: 20px;
    }
    .header-title {
        font-size: 24px;
        font-weight: 700;
        color: #0F172A;
        margin: 0;
    }
    .header-sub {
        font-size: 13px;
        color: #64748B;
        margin-top: 4px;
    }
    .badge-roll {
        background-color: #2563EB;
        color: #FFFFFF;
        padding: 3px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 12px;
        display: inline-block;
    }

    /* Metric Cards */
    .kpi-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .kpi-card:hover {
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.07);
        transform: translateY(-1px);
    }
    .kpi-label {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        color: #64748B;
        letter-spacing: 0.5px;
    }
    .kpi-value {
        font-size: 21px;
        font-weight: 700;
        color: #0F172A;
        margin: 4px 0 2px 0;
    }
    .kpi-sub {
        font-size: 11px;
        color: #10B981;
        font-weight: 500;
    }
    .kpi-sub-neutral {
        font-size: 11px;
        color: #64748B;
    }

    /* Insights Box */
    .insights-card {
        background-color: #F8FAFC;
        border-left: 4px solid #2563EB;
        border-top: 1px solid #E2E8F0;
        border-right: 1px solid #E2E8F0;
        border-bottom: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 20px;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid #E2E8F0;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #F8F9FA;
        border-radius: 6px 6px 0 0;
        border: 1px solid #E2E8F0;
        border-bottom: none;
        padding: 8px 16px;
        color: #475569;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF !important;
        border-top: 2px solid #2563EB !important;
        color: #2563EB !important;
        font-weight: 700 !important;
    }

    /* Sidebar background */
    section[data-testid="stSidebar"] {
        background-color: #F8F9FA;
        border-right: 1px solid #E2E8F0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# 3. CACHED DATA INGESTION
# -----------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_analytical_data() -> pd.DataFrame:
    """Load cleaned parquet analytical dataset."""
    if CLEAN_PARQUET_PATH.exists():
        df = pd.read_parquet(CLEAN_PARQUET_PATH)
    else:
        from src.clean import clean_ecommerce_data
        df = clean_ecommerce_data()
    
    # Ensure Order_Date is datetime
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    return df


df_master = load_analytical_data()

# -----------------------------------------------------------------------------
# 4. SIDEBAR GLOBAL FILTERS (7 SYNCHRONIZED FILTERS)
# -----------------------------------------------------------------------------
st.sidebar.markdown("### 🔍 Dashboard Filters")
st.sidebar.caption("Filter data across all KPIs and visualizations.")

# Reset Button
if st.sidebar.button("🔄 Reset All Filters", use_container_width=True):
    for key in list(st.session_state.keys()):
        if key.startswith("filter_"):
            del st.session_state[key]
    st.rerun()

st.sidebar.markdown("---")

# Filter 1: Date Range
min_order_date = df_master["Order_Date"].min().date()
max_order_date = df_master["Order_Date"].max().date()

selected_date_range = st.sidebar.date_input(
    "Order Date Range",
    value=(min_order_date, max_order_date),
    min_value=min_order_date,
    max_value=max_order_date,
    key="filter_date_range",
)

# Filter 2: Product Category
all_categories = sorted(df_master["Product_Category"].unique().tolist())
selected_categories = st.sidebar.multiselect(
    "Product Category",
    options=all_categories,
    default=[],
    placeholder="All 8 Categories",
    key="filter_categories",
)

# Filter 3: Customer Segment
all_segments = ["VIP", "Loyal", "Regular", "New"]
selected_segments = st.sidebar.multiselect(
    "Customer Segment",
    options=all_segments,
    default=[],
    placeholder="All Segments",
    key="filter_segments",
)

# Filter 4: State
all_states = sorted(df_master["State"].unique().tolist())
selected_states = st.sidebar.multiselect(
    "Customer State",
    options=all_states,
    default=[],
    placeholder="All Indian States",
    key="filter_states",
)

# Filter 5: Payment Method
all_payment_methods = sorted(df_master["Payment_Method"].unique().tolist())
selected_payments = st.sidebar.multiselect(
    "Payment Method",
    options=all_payment_methods,
    default=[],
    placeholder="All Payment Modes",
    key="filter_payments",
)

# Filter 6: Order Status
all_statuses = ["Delivered", "Shipped", "Cancelled", "Returned"]
selected_statuses = st.sidebar.multiselect(
    "Order Status",
    options=all_statuses,
    default=[],
    placeholder="All Fulfillment Statuses",
    key="filter_statuses",
)

# Filter 7: Device Channel
all_devices = sorted(df_master["Device_Type"].unique().tolist())
selected_devices = st.sidebar.multiselect(
    "Device Channel",
    options=all_devices,
    default=[],
    placeholder="All Devices",
    key="filter_devices",
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div style='font-size: 11px; color: #64748B;'>
        <b>Data Warehouse Link:</b> Star schema fact & dimension models.<br>
        <b>Net Revenue Rule:</b> Delivered & Shipped only.<br>
        <b>Evaluation:</b> Roll No. 4010 | DWBI [1ADPE404]
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 5. FILTER APPLICATION LOGIC
# -----------------------------------------------------------------------------
df_filtered = df_master.copy()

# Date filter
if isinstance(selected_date_range, tuple) and len(selected_date_range) == 2:
    start_d, end_d = selected_date_range
    df_filtered = df_filtered[
        (df_filtered["Order_Date"].dt.date >= start_d) & (df_filtered["Order_Date"].dt.date <= end_d)
    ]

# Multi-select filters
if selected_categories:
    df_filtered = df_filtered[df_filtered["Product_Category"].isin(selected_categories)]

if selected_segments:
    df_filtered = df_filtered[df_filtered["Customer_Segment"].isin(selected_segments)]

if selected_states:
    df_filtered = df_filtered[df_filtered["State"].isin(selected_states)]

if selected_payments:
    df_filtered = df_filtered[df_filtered["Payment_Method"].isin(selected_payments)]

if selected_statuses:
    df_filtered = df_filtered[df_filtered["Order_Status"].isin(selected_statuses)]

if selected_devices:
    df_filtered = df_filtered[df_filtered["Device_Type"].isin(selected_devices)]


# -----------------------------------------------------------------------------
# 6. HEADER & METADATA SECTION
# -----------------------------------------------------------------------------
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown(
        f"""
        <div class="header-container">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <h1 class="header-title">🛒 E-Commerce Customer Analytics Dashboard</h1>
                    <div class="header-sub">
                        Data Warehousing & Business Intelligence [1ADPE404] | Dept. of AI & Data Science, ADCET Ashta
                    </div>
                </div>
                <div style="text-align: right;">
                    <span class="badge-roll">Roll No. 4010</span>
                    <div style="font-size: 11px; color: #64748B; margin-top: 4px;">
                        Data Horizon: 2024–2025
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_h2:
    st.markdown(
        f"""
        <div class="header-container" style="text-align: center;">
            <div style="font-size: 11px; font-weight: 600; color: #64748B; text-transform: uppercase;">
                Filtered Dataset Size
            </div>
            <div style="font-size: 24px; font-weight: 800; color: #2563EB;">
                {len(df_filtered):,} <span style="font-size: 13px; font-weight: 400; color: #64748B;">/ 9,900</span>
            </div>
            <div style="font-size: 11px; color: #10B981; font-weight: 500;">
                {len(df_filtered) / len(df_master) * 100:.1f}% Active Scope
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------------------------------------------------------
# 7. EMPTY STATE HANDLING
# -----------------------------------------------------------------------------
if df_filtered.empty:
    st.warning(
        "⚠️ **No transactions match the selected filter criteria.** Please broaden your filter parameters or click 'Reset All Filters' in the sidebar."
    )
    st.stop()


# -----------------------------------------------------------------------------
# 8. COMPUTE ALL 13 CORE KPIS
# -----------------------------------------------------------------------------
kpi_data = compute_all_kpis(df_filtered)

# -----------------------------------------------------------------------------
# 9. KPI METRIC CARD ROWS (2 ROWS × 6 METRICS = 12 HEADLINE CARDS)
# -----------------------------------------------------------------------------
st.markdown("##### 📌 Core Financial & Commercial Performance")

# Row 1: Core Financials & Customer Base
r1_c1, r1_c2, r1_c3, r1_c4, r1_c5, r1_c6 = st.columns(6)

with r1_c1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Net Revenue</div>
            <div class="kpi-value" style="color: #2563EB;">{kpi_data['net_revenue_fmt']}</div>
            <div class="kpi-sub">Delivered & Shipped</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with r1_c2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Orders</div>
            <div class="kpi-value">{kpi_data['total_orders_fmt']}</div>
            <div class="kpi-sub-neutral">Unique Order IDs</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with r1_c3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Unique Customers</div>
            <div class="kpi-value">{kpi_data['unique_cust_fmt']}</div>
            <div class="kpi-sub-neutral">Distinct Buyer Base</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with r1_c4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Avg Order Value (AOV)</div>
            <div class="kpi-value">{kpi_data['aov_fmt']}</div>
            <div class="kpi-sub-neutral">Spend per Net Order</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with r1_c5:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Repeat Buyer Rate</div>
            <div class="kpi-value" style="color: #10B981;">{kpi_data['repeat_rate_fmt']}</div>
            <div class="kpi-sub">≥2 Completed Orders</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with r1_c6:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Average CSAT Rating</div>
            <div class="kpi-value" style="color: #F59E0B;">{kpi_data['avg_rating_fmt']}</div>
            <div class="kpi-sub-neutral">Voluntary Reviews</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Row 2: Operational Health, Discounts & Growth
r2_c1, r2_c2, r2_c3, r2_c4, r2_c5, r2_c6 = st.columns(6)

with r2_c1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Cancellation Rate</div>
            <div class="kpi-value" style="color: #EF4444;">{kpi_data['cancel_rate_fmt']}</div>
            <div class="kpi-sub-neutral">Pre-dispatch Drop-offs</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with r2_c2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Return Rate</div>
            <div class="kpi-value" style="color: #EA580C;">{kpi_data['return_rate_fmt']}</div>
            <div class="kpi-sub-neutral">Post-delivery Returns</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with r2_c3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Avg Delivery Turnaround</div>
            <div class="kpi-value">{kpi_data['avg_delivery_fmt']}</div>
            <div class="kpi-sub-neutral">Doorstep Transit Speed</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with r2_c4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Avg Promotional Disc</div>
            <div class="kpi-value">{kpi_data['avg_discount_fmt']}</div>
            <div class="kpi-sub-neutral">Pricing Concession</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with r2_c5:
    mom_color = "#10B981" if kpi_data["mom_growth_raw"] >= 0 else "#EF4444"
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">MoM Revenue Growth</div>
            <div class="kpi-value" style="color: {mom_color};">{kpi_data['mom_growth_fmt']}</div>
            <div class="kpi-sub-neutral">Latest 2-Month Trajectory</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with r2_c6:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Top Segment Share</div>
            <div class="kpi-value" style="font-size: 16px; margin-top: 8px;">{kpi_data['top_seg_fmt']}</div>
            <div class="kpi-sub-neutral">Revenue Concentration</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 10. FIVE THEMATIC DASHBOARD TABS
# -----------------------------------------------------------------------------
tab_overview, tab_customers, tab_products, tab_operations, tab_data = st.tabs(
    [
        "📈 1. Overview & Trends",
        "👥 2. Customer Analytics",
        "📦 3. Products & Merchandising",
        "🚚 4. Operations & Logistics",
        "📋 5. Data Explorer & Star Schema",
    ]
)

# -----------------------------------------------------------------------------
# TAB 1: OVERVIEW & TRENDS
# -----------------------------------------------------------------------------
with tab_overview:
    # Executive Insights Callout
    insights = generate_executive_insights(df_filtered)
    insights_html = "<br>".join([f"• {i}" for i in insights])
    st.markdown(
        f"""
        <div class="insights-card">
            <div style="font-weight: 700; color: #1E40AF; font-size: 14px; margin-bottom: 8px;">
                💡 Executive Intelligence & Actionable Insights
            </div>
            <div style="font-size: 13px; color: #1E293B; line-height: 1.6;">
                {insights_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_ov1, col_ov2 = st.columns([1.6, 1])
    with col_ov1:
        st.plotly_chart(chart_monthly_revenue(df_filtered), use_container_width=True)
    with col_ov2:
        st.plotly_chart(chart_order_status_share(df_filtered), use_container_width=True)

    st.plotly_chart(chart_category_revenue(df_filtered), use_container_width=True)


# -----------------------------------------------------------------------------
# TAB 2: CUSTOMER ANALYTICS
# -----------------------------------------------------------------------------
with tab_customers:
    col_cu1, col_cu2 = st.columns(2)
    with col_cu1:
        st.plotly_chart(chart_segment_revenue(df_filtered), use_container_width=True)
    with col_cu2:
        st.plotly_chart(chart_segment_customer_mix(df_filtered), use_container_width=True)

    col_cu3, col_cu4 = st.columns(2)
    with col_cu3:
        st.plotly_chart(chart_age_group_revenue(df_filtered), use_container_width=True)
    with col_cu4:
        st.plotly_chart(chart_repeat_vs_onetime(df_filtered), use_container_width=True)

    # Top 10 Customers Leaderboard
    st.markdown("##### 🏆 Top 10 High-Value Customers")
    net_cust = df_filtered[df_filtered["Net_Flag"] == True]
    if not net_cust.empty:
        top_cust_df = (
            net_cust.groupby(["Customer_ID", "Customer_Name", "Customer_Segment", "City", "State"])
            .agg(
                Net_Spend=("Total_Amount", "sum"),
                Completed_Orders=("Order_ID", "nunique"),
                Avg_Basket=("Total_Amount", "mean"),
            )
            .reset_index()
            .sort_values("Net_Spend", ascending=False)
            .head(10)
        )
        top_cust_df["Net_Spend"] = top_cust_df["Net_Spend"].apply(lambda x: format_inr(x, compact=False))
        top_cust_df["Avg_Basket"] = top_cust_df["Avg_Basket"].apply(lambda x: format_inr(x, compact=False))
        st.dataframe(
            top_cust_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Customer_ID": "Buyer ID",
                "Customer_Name": "Full Name",
                "Customer_Segment": "Segment",
                "City": "City",
                "State": "State",
                "Completed_Orders": "Orders Placed",
                "Net_Spend": "Total Net Spend",
                "Avg_Basket": "Average Basket Size",
            },
        )


# -----------------------------------------------------------------------------
# TAB 3: PRODUCTS & MERCHANDISING
# -----------------------------------------------------------------------------
with tab_products:
    col_pr1, col_pr2 = st.columns(2)
    with col_pr1:
        st.plotly_chart(chart_top_products(df_filtered, top_n=10), use_container_width=True)
    with col_pr2:
        st.plotly_chart(chart_category_revenue_pie(df_filtered), use_container_width=True)

    col_pr3, col_pr4 = st.columns(2)
    with col_pr3:
        st.plotly_chart(chart_discount_vs_aov(df_filtered), use_container_width=True)
    with col_pr4:
        st.plotly_chart(chart_category_monthly_trend(df_filtered), use_container_width=True)


# -----------------------------------------------------------------------------
# TAB 4: OPERATIONS & LOGISTICS
# -----------------------------------------------------------------------------
with tab_operations:
    col_op1, col_op2 = st.columns(2)
    with col_op1:
        st.plotly_chart(chart_operational_rates(df_filtered), use_container_width=True)
    with col_op2:
        st.plotly_chart(chart_payment_methods(df_filtered), use_container_width=True)

    col_op3, col_op4 = st.columns(2)
    with col_op3:
        st.plotly_chart(chart_device_types(df_filtered), use_container_width=True)
    with col_op4:
        st.plotly_chart(chart_delivery_by_state(df_filtered), use_container_width=True)

    st.plotly_chart(chart_rating_vs_delivery(df_filtered), use_container_width=True)


# -----------------------------------------------------------------------------
# TAB 5: DATA EXPLORER & STAR SCHEMA AUDIT
# -----------------------------------------------------------------------------
with tab_data:
    st.markdown("##### 🔍 Analytical Dataset Explorer")
    st.caption("Inspect filtered records and download for ad-hoc Excel or Python modeling.")

    # CSV Download Button
    csv_bytes = df_filtered.to_csv(index=False).encode("utf-8")
    col_d1, col_d2 = st.columns([1, 4])
    with col_d1:
        st.download_button(
            label="📥 Export Filtered Data (CSV)",
            data=csv_bytes,
            file_name=f"ecommerce_filtered_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with col_d2:
        st.info(
            f"Displaying **{len(df_filtered):,}** filtered rows across **{df_filtered.shape[1]}** dimensions & measures. "
            f"All values strictly adhere to the Net Revenue integrity guidelines."
        )

    # Interactive Table
    display_cols = [
        "Order_ID",
        "Order_Date",
        "Customer_Name",
        "Customer_Segment",
        "City",
        "State",
        "Product_Category",
        "Product_Name",
        "Unit_Price",
        "Quantity",
        "Discount_Pct",
        "Total_Amount",
        "Payment_Method",
        "Order_Status",
        "Delivery_Days",
        "Customer_Rating",
    ]
    st.dataframe(
        df_filtered[display_cols],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Order_Date": st.column_config.DateColumn("Date", format="YYYY-MM-DD"),
            "Unit_Price": st.column_config.NumberColumn("Unit Price", format="₹%d"),
            "Total_Amount": st.column_config.NumberColumn("Invoice Total", format="₹%.2f"),
            "Discount_Pct": st.column_config.NumberColumn("Discount", format="%d%%"),
            "Customer_Rating": st.column_config.NumberColumn("Rating", format="%.1f ★"),
        },
    )

    st.markdown("---")
    st.markdown("##### 🏛️ Data Warehouse Star Schema Dimensionality")
    sc1, sc2, sc3, sc4 = st.columns(4)
    with sc1:
        st.metric("Fact Orders Rows", f"{len(df_master):,}", "fact_orders.csv")
    with sc2:
        st.metric("Unique Customer Dimension", f"{df_master['Customer_ID'].nunique():,}", "dim_customer.csv")
    with sc3:
        st.metric("Product Dimension SKUs", f"{df_master['Product_Name'].nunique():,}", "dim_product.csv")
    with sc4:
        st.metric("Calendar Horizon Days", "731 days", "dim_date.csv (24 months)")
