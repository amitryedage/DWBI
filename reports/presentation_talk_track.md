# Presentation Talk Track & Viva Defense Guide (5–7 Minutes)

**Course:** Data Warehousing & Business Intelligence [1ADPE404]  
**Department:** Dept. of AI & Data Science, ADCET Ashta (2026-27)  
**Activity:** ISE-I Activity 2  
**Presenter:** Student, Roll No. 4010  
**Title:** E-Commerce Customer Analytics Dashboard  

---

## 1. Timed 5–7 Minute Presentation Talk Track

```
+---------------------------------------------------------------------------------------+
|  TIMELINE          |  SECTION                                |  TIME ALLOCATION       |
+---------------------------------------------------------------------------------------+
|  0:00 – 0:45       |  1. Problem Statement & Objectives      |  45 seconds            |
|  0:45 – 1:30       |  2. Dataset & KPI Architecture          |  45 seconds            |
|  1:30 – 2:30       |  3. ETL Cleansing & Star Schema Model   |  60 seconds            |
|  2:30 – 5:00       |  4. Live Dashboard Walkthrough          |  150 seconds (2.5 min) |
|  5:00 – 6:15       |  5. Quantified Executive Findings       |  75 seconds            |
|  6:15 – 7:00       |  6. Strategic Recommendations & Q&A     |  45 seconds            |
+---------------------------------------------------------------------------------------+
|  TOTAL REHEARSED DURATION: 6 MINUTES 40 SECONDS (SAFELY WITHIN 5 TO 7 MIN LIMIT)     |
+---------------------------------------------------------------------------------------+
```

---

### [0:00 – 0:45] Slide 1: Introduction & Business Problem
> *"Good morning, respected Professor and evaluators. I am presenting my Data Warehousing & Business Intelligence project for ISE-I Activity 2, titled **E-Commerce Customer Analytics Dashboard**, for Roll Number 4010.*  
>  
> *Modern e-commerce retailers capture thousands of daily transactions across diverse categories, customer segments, and geographies. However, raw spreadsheets cannot instantly answer core commercial questions: Which customer cohorts drive the highest lifetime value? Are promotional discounts expanding basket size or just cutting gross margin? Which fulfillment bottlenecks lead to returns and cancellations?*  
>  
> *The objective of this project is to build an interactive, production-ready BI dashboard backed by a dimensional data warehouse star schema that transforms raw transaction logs into executive intelligence in seconds."*

---

### [0:45 – 1:30] Slide 2: Dataset Profile & KPI Definitions
> *"Our dataset covers 10,000 synthetic e-commerce orders recorded across India from January 2024 to December 2025. It captures 20 attributes including order status, pricing, discounts, shipping turnaround, and customer review scores.*  
>  
> *In business intelligence, metrics must have airtight accounting definitions. The core foundation of our analytics is the **Net Revenue Golden Rule**: Net Revenue sums invoice totals for orders marked as **Delivered** or **Shipped** only. Orders that are **Cancelled** before dispatch or **Returned** after receipt do not represent retained cash flow and are strictly excluded from topline revenue.*  
>  
> *From this foundation, we formulated 13 core business KPIs—ranging from Average Order Value and Repeat Purchase Rate to Logistics Delivery Days and MoM Revenue Growth."*

---

### [1:30 – 2:30] Slide 3: ETL Pipeline & Star Schema Data Warehousing
> *"In Phase 2, we engineered a robust automated ETL pipeline in Python:*  
> *1. **Deduplication:** We detected and purged exactly 100 duplicate transactions, yielding 9,900 verified orders.*  
> *2. **Imputation:** Missing values in demographic fields like Gender, City, and Payment Method were filled with `'Unknown'` to avoid algorithmic bias. For Age, we imputed the median of 32.0 years and added an explicit `Age_Imputed` audit flag.*  
> *3. **Formula Audit:** We verified that `Total_Amount = Unit_Price * Quantity * (1 - Discount_Pct)` with zero discrepancies across all 9,900 rows.*  
>  
> *To align directly with Data Warehousing principles, we decomposed this flat data into a **Star Schema**:*  
> *- **`fact_orders`** stores measurable numerical facts—quantities, invoice amounts, discounts, and ratings.*  
> *- Dimensions **`dim_customer`**, **`dim_product`**, and **`dim_date`** provide the 'Who', 'What', and 'When' contexts using surrogate integer keys with 100% referential integrity."*

---

### [2:30 – 5:00] Slide 4: Live Interactive Dashboard Demonstration
*(Switch screen to the running Streamlit dashboard at `http://localhost:8501`)*

> *"Here is the live dashboard. Notice first that the application enforces a **pure white and light background theme** (`#FFFFFF` canvas with light `#F8F9FA` cards and dark `#0F172A` text), guaranteeing crisp legibility on projectors.*  
>  
> *At the top, we see the headline metrics:*  
> *- **Net Revenue:** ₹2.46 Crores across 9,900 orders.*  
> *- **Average Order Value (AOV):** ₹2,965.59.*  
> *- **Repeat Purchase Rate:** 78.8% of our 2,424 buyers placed multiple orders.*  
>  
> *On the left, we provide **7 synchronized multi-select filters**: Date Range, Category, Segment, State, Payment Mode, Status, and Device. Watch as I filter for **Customer Segment = 'VIP'**: immediately, all 12 KPI cards and charts dynamically recalculate with zero latency.*  
>  
> *Let's walk through the 5 thematic tabs:*  
> *1. **Overview:** Features the dynamic Executive Insights box, the monthly net revenue trajectory highlighting festive season spikes, and the fulfillment breakdown.*  
> *2. **Customer Analytics:** Visualizes revenue by customer segment, age cohorts, and showcases our top 10 customer leaderboard.*  
> *3. **Products & Merchandising:** Shows top 10 revenue-generating SKUs and proves the relationship between promotional discount bands and basket size.*  
> *4. **Operations & Logistics:** Tracks cancellation and return trends over time, payment methods, and correlates delivery transit speed with customer star ratings.*  
> *5. **Data Explorer & Audit:** Allows business users to inspect filtered rows and export an instant CSV download."*

---

### [5:00 – 6:15] Slide 5: Key Business Insights (Hard Numbers)
> *"From this dashboard, we extracted 5 critical business insights for executive decision-makers:*  
>  
> *1. **Festive Demand Surge:** Daily net revenue surges by **+28.4%** during the Diwali festive window (mid-October to mid-November) compared to standard months.*  
> *2. **Merchandise Dominance:** **Electronics** is our flagship category, contributing **₹77.8 Lakhs (31.6%)** of total net revenue, followed closely by Fashion.*  
> *3. **High-Value Loyalty:** **Loyal and VIP** customers account for **60.4%** of our customer base but drive **60.1% of total net revenue (₹1.48 Cr)**.*  
> *4. **Payment Channel Friction:** Orders placed via **Cash on Delivery (COD)** suffer a **10.2% cancellation rate**, significantly higher than the 6.8% seen on prepaid UPI orders.*  
> *5. **Turnaround vs. Rating Link:** Fast doorstep delivery (within **≤2 days**) achieves an average rating of **4.18 ★**, whereas orders taking **≥6 days** drop to **3.72 ★**."*

---

### [6:15 – 7:00] Slide 6: Recommendations & Conclusion
> *"Based on these findings, we recommend three strategic initiatives:*  
> *1. **Incentivize Prepaid UPI:** Offer a 3% cashback on prepaid checkouts to curb Cash-on-Delivery cancellations and Return-to-Origin losses.*  
> *2. **VIP Loyalty Tiering:** Implement exclusive festive previews and free expedited shipping for the Loyal and VIP segments to protect our primary revenue engine.*  
> *3. **Logistics SLA Tightening:** Regionalize inventory in high-volume states to ensure sub-3-day fulfillment, directly safeguarding customer satisfaction scores.*  
>  
> *As a backup and to satisfy the college notice, we also generated an offline **Excel BI Workbook** complete with pivot tables, native charts, and KPI sheets.*  
>  
> *Thank you. I am now open to your questions."*

---

## 2. Anticipated Viva Voce Questions & Model Answers

### Q1: Why did you choose Streamlit + Python instead of Power BI or Tableau?
* **Answer:** *"Streamlit enables code-based, end-to-end reproducibility. Unlike drag-and-drop proprietary BI tools, our entire ETL data pipeline, boundary validations, unit tests in pytest, and dimensional transformations live in a single version-controlled Git repository. Furthermore, we generated a comprehensive Excel backup workbook (`ecommerce_bi_backup.xlsx`) with pivot tables and charts to fully satisfy the tools mentioned in the notice."*

### Q2: Why exclude Returned and Cancelled orders from Net Revenue?
* **Answer:** *"Cancelled orders never result in cash collection or warehouse dispatch. Returned orders result in customer refunds where inventory is restored to stock. If we counted them in revenue, our topline financial figures would be artificially overstated by ~₹49 Lakhs (~16.6%), misleading management on actual profitability."*

### Q3: What is a Star Schema and where is it in your project?
* **Answer:** *"A Star Schema is an industry-standard dimensional modeling technique where a central Fact table containing quantitative business event measures is surrounded by radial Dimension tables containing descriptive context attributes. In our project, `fact_orders` contains transactional measures (Quantity, Unit Price, Invoice Amount, Rating), linked via foreign keys to `dim_customer`, `dim_product`, and `dim_date`. This structure minimizes data redundancy, prevents update anomalies, and optimizes aggregation query performance."*

### Q4: How is Repeat Purchase Rate computed?
* **Answer:** *"We group orders by `Customer_ID` and count the number of distinct orders per buyer. Customers with $\ge 2$ completed orders are divided by the total count of unique customers: $\frac{\text{Repeat Buyers (1,910)}}{\text{Total Unique Customers (2,424)}} = 78.8\%$. This proves strong platform retention."*

### Q5: How did you handle missing values, and why?
* **Answer:** *"We used principled, domain-appropriate rules:
  - `Gender`, `City`, and `Payment_Method` were filled with `'Unknown'` to avoid introducing artificial bias or guessing sensitive demographic information.
  - `Age` was imputed with the median (32.0 years) because median is resilient to skew, and we preserved transparency by adding an `Age_Imputed` audit flag.
  - `Delivery_Days` and `Customer_Rating` were intentionally preserved as blank for unfulfilled or unreviewed orders. Defaulting them to zero would severely skew average delivery turnaround and crush customer satisfaction metrics."*

### Q6: What does the Discount vs. AOV chart tell the business?
* **Answer:** *"It visualizes price elasticity and promotional effectiveness. While promotions increase order volumes, heavy discounts (>30%) do not proportionally increase basket size. Moderate discounts (10–20%) achieve the optimal balance between customer acquisition and order value retention."*

### Q7: If given real production enterprise data, how would this architecture adapt?
* **Answer:** *"Our architecture is fully modular. The ETL pipeline (`clean.py`) and Star Schema generator (`schema.py`) take any CSV or database extraction matching the schema. To connect to an enterprise warehouse like Snowflake or BigQuery, we would simply replace `pd.read_parquet` with an SQLAlchemy / Snowflake connector; the KPI computation engine and Streamlit visualizations would remain 100% reusable."*

### Q8: What stretch features could be added next?
* **Answer:** *"1. RFM (Recency, Frequency, Monetary) segmentation to identify churn-risk customers. 2. Cohort retention heatmaps. 3. Machine learning time-series forecasting (Prophet or ARIMA) to predict next-quarter inventory demand."*
