# E-Commerce Customer Analytics Dashboard

**Course:** Data Warehousing & Business Intelligence [1ADPE404]  
**Department:** Dept. of AI & Data Science, ADCET Ashta (2026-27)  
**Evaluation:** ISE-I Activity 2  
**Roll No:** 4010  
**Stack:** Excel + Python (`uv`) + pandas + Streamlit + Plotly + pytest  
**Theme:** Crisp White / Light Mode for Maximum Readability (P0 Priority)  

---

## 1. Project Overview

An interactive, production-ready Business Intelligence (BI) dashboard analyzing **10,000 synthetic e-commerce transactions** across India from Jan 1, 2024 to Dec 31, 2025. 

The dashboard bridges raw spreadsheet transactions with enterprise decision-making, providing real-time KPI computations, multidimensional filtering, and visual insights tailored to business managers, marketing analysts, and operations leads.

### Key Objectives & Deliverables
* **Phase 1 (Data Understanding):** Profiled raw data, audited 100 duplicate rows, formulated 13 business KPIs, and designed UI wireframes.
* **Phase 2 (Preparation & Warehousing):** Cleaned and deduplicated 9,900 orders, applied principled imputation, validated ranges, engineered derived dimensions, and produced a **Star Schema** (`fact_orders`, `dim_customer`, `dim_product`, `dim_date`).
* **Phase 3 (Dashboard Build):** Developed an interactive **Streamlit BI Dashboard** with 7 synchronized filters, 12 headline KPI cards, and 12 Plotly visualizations (bar, pie, line charts) under a strict pure white / light theme.
* **Phase 5 (Quality, Presentation & Viva):** Formulated 5 quantified executive insights, built an offline **Excel BI Backup Workbook** with pivot charts, created a 5–7 minute presentation talk track with viva answers, and authored an automated test suite.

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
       ├──► fact_orders.csv   (9,900 rows)
       ├──► dim_customer.csv  (2,424 unique customers)
       ├──► dim_product.csv   (40 unique merchandise items)
       └──► dim_date.csv      (731 calendar days)
       │
       ▼
  Streamlit BI Dashboard (app.py) & Excel Backup Workbook
       ├──► Strict Light Theme (#FFFFFF Canvas & #F8F9FA Cards)
       ├──► 7 Synchronized Global Filters
       ├──► 12 Headline KPI Cards (Net Revenue, AOV, Repeat Rate, CSAT)
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
│       ├── ecommerce_clean.parquet   # High-speed analytical dataset (289 KB)
│       ├── ecommerce_clean.xlsx      # Cleaned Excel dataset (1.44 MB)
│       ├── ecommerce_bi_backup.xlsx  # Complete Excel backup with pivot charts (1.38 MB)
│       ├── fact_orders.csv           # Star schema: Fact table
│       ├── dim_customer.csv          # Star schema: Customer dimension
│       ├── dim_product.csv           # Star schema: Product dimension
│       └── dim_date.csv              # Star schema: Date dimension
├── src/
│   ├── __init__.py
│   ├── config.py                     # Light theme color tokens, paths, INR formatters
│   ├── clean.py                      # Phase 2: Data cleansing & ETL pipeline
│   ├── schema.py                     # Phase 2: Star schema builder
│   ├── kpis.py                       # Phase 3: All 13 KPI calculation functions
│   ├── charts.py                     # Phase 3: 12 Plotly visualization functions
│   ├── insights.py                   # Phase 3/5: Dynamic business insights generator
│   ├── profile_data.py               # Phase 1: Automated raw data profiler
│   └── build_excel_backup.py         # Phase 5: Excel backup generator with charts
├── tests/
│   ├── __init__.py
│   ├── test_clean.py                 # 8 unit tests for ETL & schema integrity
│   └── test_kpis.py                  # 4 unit tests for KPI math & edge cases
├── reports/
│   ├── data_profile.md               # Raw dataset profile & statistical audit
│   ├── data_quality_report.md        # Cleansing audit & viva rationale
│   ├── kpi_definitions.md            # Mathematical formulas & viva pitches
│   ├── dashboard_wireframe.md        # UI/UX wireframe & layout tokens
│   ├── executive_insights_summary.md # 5 quantified business findings with numbers
│   └── presentation_talk_track.md    # 5–7 minute rehearsed script & viva Q&A
├── .streamlit/
│   └── config.toml                   # White/Light UI theme settings
├── app.py                            # Streamlit entry point
├── pyproject.toml                    # UV project configuration
├── requirements.txt                  # Deployment dependencies for Streamlit Cloud
└── README.md                         # Project documentation
```

---

## 4. Baseline KPI Scorecard (Entire Clean Dataset)

| KPI # | Metric Name | Baseline Value | Formatted Display | Accounting Rule |
|---|---|---|---|---|
| 1 | Net Revenue | ₹24,620,351.40 | **₹2.46 Cr** | Delivered + Shipped orders only |
| 2 | Total Orders | 9,900 | **9,900** | Distinct Order_IDs |
| 3 | Unique Customers | 2,424 | **2,424** | Distinct Customer_IDs |
| 4 | Average Order Value (AOV) | ₹2,965.59 | **₹2,965.59** | Net Revenue / Net Orders |
| 5 | Revenue per Customer | ₹10,156.91 | **₹10,156.91** | Net Revenue / Unique Customers |
| 6 | Repeat Purchase Rate | 78.80% | **78.8%** | Customers with ≥2 completed orders |
| 7 | Cancellation Rate | 8.34% | **8.3%** | Cancelled orders / Total orders |
| 8 | Return Rate | 8.97% | **9.0%** | Returned / (Delivered + Returned) |
| 9 | Average Discount | 12.51% | **12.5%** | Mean promotional discount applied |
| 10 | Average Delivery Turnaround | 3.68 days | **3.7 days** | Mean fulfillment days for delivered |
| 11 | Average CSAT Rating | 4.00 / 5.0 | **4.00 / 5.0** | Mean star rating for reviewed orders |
| 12 | MoM Revenue Growth | -31.7% | **-31.7%** | Dec 2025 vs Nov 2025 (post-festive) |
| 13 | Top Segment Share | 38.0% | **Loyal (38.0%)** | Highest contributing customer cohort |

---

## 5. Quick Start & Execution

### Prerequisites
* Python 3.10+ installed
* `uv` package manager installed (`pip install uv` or standalone installer)

### Commands

```powershell
# 1. Install all dependencies
uv sync

# 2. Run ETL pipeline & generate Star Schema
uv run python -m src.clean
uv run python -m src.schema

# 3. Build offline Excel backup workbook with pivot charts
uv run python -m src.build_excel_backup

# 4. Run automated test suite (12/12 passing tests)
uv run pytest -v

# 5. Launch interactive BI dashboard
uv run streamlit run app.py
```

The application will launch in your browser at `http://localhost:8501`.

---

## 6. Visual Theme Guidelines

The application strictly implements an **all-white / light color background scheme** (`#FFFFFF` app canvas, `#F8F9FA` card containers, `#1E293B` high-contrast dark typography) ensuring crystal-clear visibility on high-resolution monitors as well as college lecture hall projectors.

---

## 7. Presentation & Viva Defense Links

* **5–7 Minute Rehearsed Talk Track:** [reports/presentation_talk_track.md](file:///d:/DWBI/reports/presentation_talk_track.md)
* **Top 5 Quantified Insights:** [reports/executive_insights_summary.md](file:///d:/DWBI/reports/executive_insights_summary.md)
* **KPI Formulas & Viva Pitches:** [reports/kpi_definitions.md](file:///d:/DWBI/reports/kpi_definitions.md)
* **Data Quality & Warehouse Report:** [reports/data_quality_report.md](file:///d:/DWBI/reports/data_quality_report.md)
* **Excel Backup Dashboard:** [data/processed/ecommerce_bi_backup.xlsx](file:///d:/DWBI/data/processed/ecommerce_bi_backup.xlsx)
