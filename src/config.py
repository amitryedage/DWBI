"""Configuration module for E-Commerce Customer Analytics Dashboard.

Defines all paths, light-theme color palettes, and formatting constants.
Adheres strictly to the white / light background requirement (P0).
"""

from pathlib import Path

# Base Directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_PATH = DATA_DIR / "raw" / "ecommerce_data.xlsx"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Processed analytical outputs
CLEAN_PARQUET_PATH = PROCESSED_DATA_DIR / "ecommerce_clean.parquet"
CLEAN_EXCEL_PATH = PROCESSED_DATA_DIR / "ecommerce_clean.xlsx"
FACT_ORDERS_PATH = PROCESSED_DATA_DIR / "fact_orders.csv"
DIM_CUSTOMER_PATH = PROCESSED_DATA_DIR / "dim_customer.csv"
DIM_PRODUCT_PATH = PROCESSED_DATA_DIR / "dim_product.csv"
DIM_DATE_PATH = PROCESSED_DATA_DIR / "dim_date.csv"

# Reports directory
REPORTS_DIR = BASE_DIR / "reports"
DATA_QUALITY_REPORT_PATH = REPORTS_DIR / "data_quality_report.md"
DATA_PROFILE_REPORT_PATH = REPORTS_DIR / "data_profile.md"
KPI_DEFINITIONS_PATH = REPORTS_DIR / "kpi_definitions.md"

# Visual Theme Specification (Pure White / Light Mode)
PLOTLY_TEMPLATE = "plotly_white"
COLOR_BG = "#FFFFFF"
COLOR_SECONDARY_BG = "#F8F9FA"
COLOR_BORDER = "#E2E8F0"
COLOR_TEXT_PRIMARY = "#0F172A"
COLOR_TEXT_SECONDARY = "#64748B"
COLOR_PRIMARY_BLUE = "#2563EB"

# Status Semantic Colors
STATUS_COLORS = {
    "Delivered": "#10B981",  # Emerald Green
    "Shipped": "#F59E0B",    # Amber
    "Returned": "#EF4444",   # Coral Red
    "Cancelled": "#94A3B8",  # Neutral Slate
}

# Customer Segment Colors
SEGMENT_COLORS = {
    "VIP": "#7C3AED",       # Deep Purple
    "Loyal": "#2563EB",     # Royal Blue
    "Regular": "#0D9488",   # Teal
    "New": "#F59E0B",       # Warm Amber
}

# Categorical Color Palette (Curated for pure white / light canvas contrast)
CATEGORICAL_PALETTE = [
    "#2563EB",  # Royal Blue
    "#0D9488",  # Teal
    "#7C3AED",  # Purple
    "#EA580C",  # Orange
    "#0284C7",  # Sky Blue
    "#16A34A",  # Forest Green
    "#DB2777",  # Magenta
    "#CA8A04",  # Ochre Yellow
    "#4F46E5",  # Indigo
    "#64748B",  # Slate
]


def format_inr(value: float, compact: bool = True) -> str:
    """Format floating point numbers into Indian Rupee strings.
    
    Examples:
        29500000 -> ₹2.95 Cr
        4500000  -> ₹45.00 Lakh
        12500    -> ₹12,500
    """
    if value is None or value != value:  # checks NaN
        return "₹0"
    
    abs_val = abs(value)
    sign = "-" if value < 0 else ""
    
    if compact:
        if abs_val >= 10_000_000:
            return f"{sign}₹{abs_val / 10_000_000:.2f} Cr"
        elif abs_val >= 100_000:
            return f"{sign}₹{abs_val / 100_000:.2f} L"
        else:
            return f"{sign}₹{abs_val:,.0f}"
    else:
        return f"{sign}₹{abs_val:,.2f}"


def format_percent(value: float, decimals: int = 1) -> str:
    """Format float into percentage string."""
    if value is None or value != value:
        return "0.0%"
    return f"{value:.{decimals}f}%"
