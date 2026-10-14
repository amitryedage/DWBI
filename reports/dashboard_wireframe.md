# Dashboard Layout & Wireframe Specification

**Course:** Data Warehousing & Business Intelligence [1ADPE404]  
**Project:** E-Commerce Customer Analytics Dashboard (Roll No. 4010)  
**Theme:** Crisp Light / Pure White Mode (P0 Priority)

---

## 1. Visual Theme & Palette Architecture

To guarantee superior clarity on lecture hall projectors, classroom screens, and viva evaluations:
* **Background Canvas:** Pure White (`#FFFFFF`).
* **Secondary Surface / Sidebar / Cards:** Soft Off-White (`#F8F9FA`).
* **Card Borders / Dividers:** Subtle Border Gray (`#E2E8F0`).
* **Primary Typography:** Slate / Midnight Charcoal (`#0F172A` and `#1E293B`).
* **Muted Typography / Captions:** Neutral Slate (`#64748B`).
* **Brand / Primary Accent:** Royal Blue (`#2563EB`).
* **Semantic Accents:**
  * Success / Delivered: Emerald (`#10B981`)
  * Warning / Shipped: Amber (`#F59E0B`)
  * Danger / Cancelled / Returned: Crimson (`#EF4444`)
  * Secondary Category Accents: Teal (`#0D9488`), Violet (`#8B5CF6`)
* **Chart Template:** Plotly `plotly_white` with clean `#E2E8F0` gridlines and transparent chart margins.

---

## 2. High-Level Page Wireframe

```
+---------------------------------------------------------------------------------------------------------+
|                                    HEADER & METADATA SECTION                                            |
| [Icon] E-COMMERCE CUSTOMER ANALYTICS DASHBOARD | Roll No. 4010                                          |
| Data Period: 01 Jan 2024 to 31 Dec 2025 | Last Refreshed: [Dynamic Timestamp] | Theme: Light Mode     |
+---------------------------------------------------------------------------------------------------------+
| SIDEBAR FILTERS           | MAIN CONTENT AREA                                                           |
|                           |                                                                             |
| [Date Range Slider]       | +-------------------------------------------------------------------------+ |
| 2024-01-01 - 2025-12-31   | | KPI ROW 1 (Core Financials & Customers)                                 | |
|                           | | [Net Revenue]  [Total Orders]  [Unique Cust]  [AOV]  [Repeat %] [Avg Rating] |
| [Product Category]        | +-------------------------------------------------------------------------+ |
| [x] All / Multi-select    | +-------------------------------------------------------------------------+ |
|                           | | KPI ROW 2 (Operations, Growth & Engagement)                              | |
| [State / City]            | | [Cancel %]   [Return %]   [Avg Delivery]  [Avg Disc %] [MoM %] [Rev/Cust] | |
| [x] All Indian Regions    | +-------------------------------------------------------------------------+ |
|                           |                                                                             |
| [Customer Segment]        | +-------------------------------------------------------------------------+ |
| [x] New, Regular, ...     | | TABS NAVIGATION:                                                        | |
|                           | | [1. Overview]  [2. Customers]  [3. Products]  [4. Operations] [5. Data] | |
| [Payment Method]          | +-------------------------------------------------------------------------+ |
| [x] UPI, Cards, COD, ...  |                                                                             |
|                           | === TAB 1: OVERVIEW ===                                                     |
| [Order Status]            | [Dynamic Executive Insights Alert Box: 5 Key Business Findings]           |
| [x] Delivered, Shipped... |                                                                             |
|                           | +-------------------------------------+ +---------------------------------+ |
| [Device Type]             | | V1: Monthly Net Revenue Trend       | | V3: Revenue by Category (Bar)   | |
| [x] App, Web, Desktop     | | (Line Chart with Festive Callouts)  | |                                 | |
|                           | +-------------------------------------+ +---------------------------------+ |
| [--- Reset Filters ---]   | +-------------------------------------------------------------------------+ |
|                           | | V7: Order Status Share (Donut / Pie Chart)                              | |
|                           | +-------------------------------------------------------------------------+ |
|                           |                                                                             |
|                           | === TAB 2: CUSTOMERS ===                                                    |
|                           | +-------------------------------------+ +---------------------------------+ |
|                           | | V4: Revenue by Customer Segment     | | V9: Customer Count by Segment   | |
|                           | +-------------------------------------+ +---------------------------------+ |
|                           | +-------------------------------------+ +---------------------------------+ |
|                           | | V12: Net Revenue by Age Group       | | Repeat vs One-Time Buyers       | |
|                           | +-------------------------------------+ +---------------------------------+ |
|                           | | Top 10 Customers Leaderboard Table                                      | |
|                           | +-------------------------------------------------------------------------+ |
|                           |                                                                             |
|                           | === TAB 3: PRODUCTS ===                                                     |
|                           | +-------------------------------------+ +---------------------------------+ |
|                           | | V6: Top 10 Revenue Products (Bar)   | | Category Revenue Share (Pie)    | |
|                           | +-------------------------------------+ +---------------------------------+ |
|                           | +-------------------------------------+ +---------------------------------+ |
|                           | | V10: Discount Band vs AOV (Bar)     | | V2: Monthly Category Trends     | |
|                           | +-------------------------------------+ +---------------------------------+ |
|                           |                                                                             |
|                           | === TAB 4: OPERATIONS ===                                                   |
|                           | +-------------------------------------+ +---------------------------------+ |
|                           | | V11: Monthly Cancel & Return Rate   | | V8: Payment Method Share (Pie)  | |
|                           | +-------------------------------------+ +---------------------------------+ |
|                           | +-------------------------------------+ +---------------------------------+ |
|                           | | Delivery Days by State (Bar)        | | Delivery Days vs Customer Rating| |
|                           | +-------------------------------------+ +---------------------------------+ |
|                           |                                                                             |
|                           | === TAB 5: DATA EXPLORER & AUDIT ===                                        |
|                           | [Summary Statistics | Row Count: 9,900 rows] [Export Filtered Data as CSV] |
|                           | [Interactive AgGrid / Streamlit Dataframe Table]                            |
+---------------------------------------------------------------------------------------------------------+
```

---

## 3. Responsiveness & Projector Optimization

1. **Card Layout:** Uses 6 columns per KPI row on standard 1080p desktop / projector view, gracefully stacking on narrower screens.
2. **Chart Contrast:** Gridlines are rendered in light slate `#E2E8F0`, and line traces use high stroke widths (minimum 2.5px) for clear visibility from back rows.
3. **Empty States:** When a filter combination returns zero records, an empty-state card rendered in soft amber `#FEF3C7` informs the user gently without red error traces.
