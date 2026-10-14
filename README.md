# E-Commerce Customer Analytics Dashboard

**Course:** Data Warehousing & Business Intelligence [1ADPE404]  
**Department:** Dept. of AI & Data Science, ADCET Ashta (2026-27)  
**Evaluation:** ISE-I Activity 2  
**Roll No:** 4010  
**Stack:** Excel + Python (`uv`) + pandas + Streamlit + Plotly + pytest  
**Theme:** Crisp White / Light Mode for High Readability  

---

## 1. Project Overview

An interactive, production-ready Business Intelligence (BI) dashboard analyzing **10,000 synthetic e-commerce transactions** across India from Jan 1, 2024 to Dec 31, 2025. 

The dashboard bridges raw spreadsheet transactions with enterprise decision-making, providing real-time KPI computations, multidimensional filtering, and visual insights tailored to business managers, marketing analysts, and operations leads.

### Key Objectives
* Clean, deduplicate, and validate raw transactions (`data/raw/ecommerce_data.xlsx`).
* Implement a Data Warehousing **Star Schema** (`fact_orders`, `dim_customer`, `dim_product`, `dim_date`).
* Compute **13 core business KPIs** adhering to the strict Net Revenue rule (Delivered/Shipped only).
* Deliver an interactive **Streamlit BI Dashboard** with 7 synchronized filters, 12 KPI cards, and 12 Plotly visualizations (bar, pie, line charts).
* Provide complete backup assets (clean Excel workbook with Pivot Tables & Charts).

---

## 2. Architecture & Star Schema

```
Raw Excel (10,000 orders)
       │
       ▼
   clean.py (Data Cleansing & Validation)
       │
       ├──► Deduplication (removes 100 duplicate rows -> 9,900 clean rows)
       ├──► Missing Value Imputation (Gender, Age, City, Payment Method)
       └──► Derived Dimensions (Year, Month, Age Group, Discount Band)
       │
       ▼
   schema.py (Star Schema Transformation)
       │
       ├──► fact_orders.csv
       ├──► dim_customer.csv
       ├──► dim_product.csv
       └──► dim_date.csv
       │
       ▼
  Streamlit BI Dashboard (app.py)
       ├──► Light Theme (#FFFFFF Canvas & #F8F9FA Cards)
       ├──► 7 Synchronized Global Filters
       ├──► 12 Headline KPI Cards
       └──► 5 Thematic Analysis Tabs
```

---

## 3. Project Directory Structure

```
DWBI/
├── data/
│   ├── raw/
│   │   └── ecommerce_data.xlsx       # Source raw transactional dataset
│   └── processed/
│       ├── ecommerce_clean.parquet   # High-speed analytical dataset
│       ├── ecommerce_clean.xlsx      # Cleaned Excel dataset
│       ├── fact_orders.csv           # Fact table
│       ├── dim_customer.csv          # Customer dimension
│       ├── dim_product.csv           # Product dimension
│       └── dim_date.csv              # Date dimension
├── src/
│   ├── __init__.py
│   ├── config.py                     # Light theme constants, colors, file paths
│   ├── clean.py                      # Data cleansing & ETL pipeline
│   ├── schema.py                     # Star schema builder
│   ├── kpis.py                       # All 13 KPI metric calculation functions
│   └── charts.py                     # Plotly chart generation functions
├── tests/
│   ├── test_clean.py                 # Data validation & cleansing tests
│   └── test_kpis.py                  # Unit tests for KPI calculations
├── reports/
│   ├── data_profile.md               # Dataset profile & statistical audit
│   ├── data_quality_report.md        # Cleansing audit & missing value rules
│   ├── kpi_definitions.md            # Formulas, business logic & Viva pitches
│   └── dashboard_wireframe.md        # UI/UX layout, wireframe & color tokens
├── .streamlit/
│   └── config.toml                   # White/Light UI theme settings
├── app.py                            # Streamlit entry point
├── pyproject.toml                    # UV project configuration & dependencies
├── README.md                         # Project documentation
└── .gitignore
```

---

## 4. Quick Start & Execution

### Prerequisites
* Python 3.10+ installed
* `uv` package manager installed (`pip install uv` or official standalone installer)

### Commands

```powershell
# 1. Install dependencies
uv sync

# 2. Run ETL pipeline (Cleans data & generates Star Schema)
uv run python -m src.clean

# 3. Run automated tests
uv run pytest

# 4. Launch interactive dashboard
uv run streamlit run app.py
```

The application will launch in your browser at `http://localhost:8501`.

---

## 5. Visual Theme Guidelines

The application strictly implements an **all-white / light color background scheme** (`#FFFFFF` app canvas, `#F8F9FA` card containers, `#1E293B` high-contrast dark typography) ensuring crystal-clear visibility on high-resolution monitors as well as college lecture hall projectors.
