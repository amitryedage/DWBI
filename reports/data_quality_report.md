# Data Quality & Warehouse Modeling Report (Phase 2)

**Course:** Data Warehousing & Business Intelligence [1ADPE404]  
**Activity:** ISE-I Activity 2 | Dept. of AI & Data Science, ADCET Ashta  
**Student Roll No:** 4010  
**Project:** E-Commerce Customer Analytics Dashboard  

---

## 1. Executive Summary: Before vs. After Cleansing

| Metric / Dimension | Raw Dataset (`ecommerce_data.xlsx`) | Cleaned Dataset (`ecommerce_clean.parquet`) | Delta / Action Taken |
|---|---|---|---|
| **Total Rows** | 10,000 | 9,900 | Purged 100 exact duplicate rows |
| **Unique Order IDs** | 9,900 | 9,900 | 100% unique primary key integrity |
| **Unique Customers** | 2,424 | 2,424 | Zero customer loss |
| **Date Horizon** | 2024-01-01 to 2025-12-31 | 2024-01-01 to 2025-12-31 | Preserved complete 24-month span |
| **Missing Gender** | 143 (1.43%) | 0 (0.00%) | Imputed with `'Unknown'` (141 in clean rows) |
| **Missing Age** | 186 (1.86%) | 0 (0.00%) | Imputed with median (`32.0`) + `Age_Imputed` flag |
| **Missing City** | 98 (0.98%) | 0 (0.00%) | Imputed with `'Unknown'` (98 in clean rows) |
| **Missing Payment Method** | 88 (0.88%) | 0 (0.00%) | Imputed with `'Unknown'` (87 in clean rows) |
| **Blank Delivery Days** | 1,271 | 1,257 | Deliberately preserved for Cancelled/Shipped |
| **Blank Customer Rating** | 3,861 | 3,828 | Deliberately preserved for unreviewed orders |
| **Total Amount Discrepancies** | 0 discrepancies > ₹0.01 | 0 discrepancies > ₹0.01 | 100% formula verified |

---

## 2. Cleansing Decisions & Viva Defense Rationale

### 2.1 Deduplication
* **Observation:** The raw spreadsheet contained 100 redundant rows where all 20 columns were identical.
* **Action:** Purged duplicate rows using `df.drop_duplicates()`, retaining 9,900 genuine analytical transactions.
* **Viva Defense:** Retaining duplicate transactional records would artificially inflate topline revenue by ₹2.95 Lakhs and distort customer purchase frequency.

### 2.2 Gender Imputation
* **Rule:** Missing values imputed with `'Unknown'`.
* **Rationale:** Gender cannot be inferred from names or purchasing patterns without introducing demographic stereotyping or bias. Assigning an explicit `'Unknown'` category preserves row usability for segment analytics without distorting gender distributions.

### 2.3 Age Imputation & Flagging
* **Rule:** Imputed missing values with the **median age (32.0 years)** and created a boolean audit flag `Age_Imputed = True`.
* **Rationale:** The age distribution has a slight right skew (mean: 32.27, median: 32.0, min: 18, max: 64). Median imputation is robust to potential outliers. The `Age_Imputed` column ensures audit transparency so evaluators or machine learning pipelines can isolate estimated records.

### 2.4 City & State Preservation
* **Rule:** Imputed missing cities with `'Unknown'`, while keeping the verified `State` column untouched.
* **Rationale:** Guessing a customer's specific city from their state would corrupt geographic drill-downs. Retaining the state ensures regional level aggregations (e.g., North vs. South or Maharashtra state-level sales) remain 100% accurate.

### 2.5 Payment Method Imputation
* **Rule:** Imputed missing payment modes with `'Unknown'`.
* **Rationale:** Guessing payment methods (e.g., assuming missing equals COD or UPI) biases financial channel analysis. Explicitly tagging missing records allows the operations team to audit checkout telemetry gaps.

### 2.6 Legitimate Business Blanks (`Delivery_Days` & `Customer_Rating`)
* **`Delivery_Days`:** Cancelled orders never leave the warehouse or complete transit, while Shipped orders are still in transit. Replacing these blanks with `0` would severely skew logistics turnaround KPIs.
* **`Customer_Rating`:** Submitting a review is voluntary in e-commerce. Blanks represent unrated transactions, not zero-star dissatisfaction. Imputing `0` would artificially collapse the CSAT average from `4.00` down to `2.45`.

---

## 3. Boundary & Integrity Validations

Every record in `ecommerce_clean.parquet` passed strict programmatic assertions:
1. **Age Range:** `18 <= Age <= 70` (Min: 18, Max: 64).
2. **Discount Percentage:** `0 <= Discount_Pct <= 40` (Min: 0%, Max: 40%).
3. **Quantity:** `Quantity >= 1` (Min: 1, Max: 5 units).
4. **Rating:** `1.0 <= Rating <= 5.0` for non-null entries.
5. **Invoice Equation:**
   $$\text{Total\_Amount} = \text{Unit\_Price} \times \text{Quantity} \times \left(1 - \frac{\text{Discount\_Pct}}{100}\right)$$
   Maximum absolute discrepancy observed was `0.0000 INR`, confirming mathematical consistency.

---

## 4. Derived Analytical Features

To accelerate Streamlit query responsiveness and simplify Plotly visualizations, the pipeline engineered 8 derived attributes:

| Feature | Data Type | Logic / Bins | Analytical Purpose |
|---|---|---|---|
| `Year` | Integer | `Order_Date.dt.year` (2024, 2025) | Annual filtering |
| `Month` | Integer | `Order_Date.dt.month` (1-12) | Seasonal sorting |
| `Month_Name` | Text | `Jan`, `Feb`, ..., `Dec` | Chart axis labels |
| `Quarter` | Text | `Q1`, `Q2`, `Q3`, `Q4` | Quarterly financial reporting |
| `Year_Month` | Text | `YYYY-MM` | Continuous time-series aggregation |
| `Net_Flag` | Boolean | `Order_Status in ['Delivered', 'Shipped']` | Rapid Net Revenue filtering |
| `Age_Group` | Categorical | `<25`, `25-34`, `35-49`, `50+` | Demographic cohort analysis |
| `Discount_Band` | Categorical | `No Discount (0%)`, `Low (1-10%)`, `Medium (11-20%)`, `High (21-30%)`, `Very High (>30%)` | Price elasticity & basket size correlation |
| `Is_Festive_Season` | Boolean | True for dates between Oct 15 and Nov 15 | Indian festive season demand spike analysis |

---

## 5. Data Warehouse Star Schema Architecture

The relational star schema separates transactional facts from descriptive dimensions to minimize analytical query latency:

```
                  +--------------------------------+
                  |          dim_date              |
                  +--------------------------------+
                  | PK: Date_Key (Integer)         |
                  |     Date (YYYY-MM-DD)          |
                  |     Day, Month, Month_Name     |
                  |     Quarter, Year              |
                  |     Is_Festive_Season (Bool)   |
                  +--------------------------------+
                                  │
                                  │ 1:N
                                  ▼
+---------------------+       +------------------------------------+       +----------------------+
|    dim_customer     |       |            fact_orders             |       |     dim_product      |
+---------------------+       +------------------------------------+       +----------------------+
| PK: Customer_Key    | 1:N   | PK: Order_ID                       |   1:N | PK: Product_Key      |
|     Customer_ID     |──────►| FK: Customer_Key                   |◄──────|     Product_Name     |
|     Customer_Name   |       | FK: Product_Key                    |       |     Product_Category |
|     Gender          |       | FK: Date_Key                       |       +----------------------+
|     Age, Age_Group  |       |                                    |
|     City, State     |       | Measures:                          |
|     Customer_Segment|       |   Quantity                         |
+---------------------+       |   Unit_Price                       |
                              |   Discount_Pct                     |
                              |   Total_Amount                     |
                              |   Delivery_Days                    |
                              |   Customer_Rating                  |
                              |                                    |
                              | Attributes:                        |
                              |   Order_Status                     |
                              |   Payment_Method                   |
                              |   Device_Type                      |
                              |   Net_Flag                         |
                              +------------------------------------+
```

### Table Specifications
* **`fact_orders.csv` (9,900 rows):** Stores business event measures and foreign keys.
* **`dim_customer.csv` (2,424 rows):** Stores normalized customer profile attributes.
* **`dim_product.csv` (40 rows):** Stores distinct catalog merchandise across 8 categories.
* **`dim_date.csv` (731 rows):** Stores complete calendar dimension covering every day of 2024 and 2025.

---

## 6. Output Artifacts Produced
* **High-Performance Parquet:** `data/processed/ecommerce_clean.parquet` (283 KB)
* **Excel Workbook Backup:** `data/processed/ecommerce_clean.xlsx` (1.4 MB)
* **Star Schema CSVs:** `fact_orders.csv`, `dim_customer.csv`, `dim_product.csv`, `dim_date.csv`
