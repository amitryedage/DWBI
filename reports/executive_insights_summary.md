# Executive Business Intelligence Insights & Findings

**Project:** E-Commerce Customer Analytics Dashboard  
**Course:** Data Warehousing & Business Intelligence [1ADPE404] | Roll No. 4010  
**Data Scope:** 9,900 Clean Transactions (2024-01-01 to 2025-12-31)  
**Total Realized Net Revenue:** ₹2.46 Crores  

---

## 1. Top 5 Quantified Business Findings

### 1. Seasonal Demand Surge (+28.4% Festive Spike)
* **Finding:** Transaction volume and daily net revenue show pronounced seasonal acceleration during the Indian festive period (mid-October to mid-November, encompassing Diwali and Dussehra).
* **Metric:** Daily average net revenue surges to **₹43,850/day** during the festive window compared to **₹34,150/day** during off-peak periods, representing a **+28.4% demand surge**.
* **Recommendation:** Ramp up inventory procurement 45 days prior to October and schedule dedicated marketing campaigns to capitalize on high festive purchase intent.

### 2. Category Concentration (Electronics Contributes 31.6% of Net Revenue)
* **Finding:** While catalog offerings span 8 product categories, revenue generation is highly concentrated in tech and apparel.
* **Metric:** **Electronics** is the leading category, contributing **₹77.8 Lakhs (31.6%)** of total net revenue, followed by **Fashion (₹51.2 Lakhs, 20.8%)**. Together, these two categories generate more than **52.4%** of company revenue.
* **Recommendation:** Negotiate bulk vendor volume rebates for high-velocity electronics SKUs and optimize logistics packaging for fragile gadgets.

### 3. Customer Base Pareto Effect (Loyal & VIP Generate 60.1% of Revenue)
* **Finding:** High-tier customer segments demonstrate superior lifetime spend and transaction consistency.
* **Metric:** **Loyal (37.9%)** and **VIP (22.5%)** customers account for **60.4%** of all unique shoppers, but contribute **₹1.48 Crores (60.1%)** of total net revenue.
* **Recommendation:** Institute an exclusive tier-based loyalty rewards program offering priority delivery and early access sales to insulate the VIP and Loyal customer base against competitive poaching.

### 4. Operational Friction & Cash on Delivery (COD) Vulnerability
* **Finding:** Overall order cancellation rate stands at **8.3%**, but checkout payment channel choice is strongly correlated with fulfillment drop-offs.
* **Metric:** Orders placed via **Cash on Delivery (COD)** suffer an elevated cancellation rate of **10.2%**, compared to only **6.8%** for prepaid UPI transactions and **7.1%** for credit cards.
* **Recommendation:** Offer a 2% to 3% instant checkout discount or cashback for customers choosing instant UPI payments to reduce Return-to-Origin (RTO) shipping overhead.

### 5. Delivery Turnaround Directly Dictates Customer CSAT Ratings
* **Finding:** Doorstep logistics velocity has a clear, measurable impact on post-purchase star reviews.
* **Metric:** Orders delivered rapidly within **≤2 days** achieve an average rating of **4.18 ★**. Orders fulfilled within standard transit times (**3–4 days**) average **4.04 ★**, while delayed deliveries taking **≥6 days** collapse to **3.72 ★**.
* **Recommendation:** Partner with regional 3PL logistics couriers in high-density delivery hubs (Maharashtra, Karnataka, Delhi NCR) with strict SLAs guaranteeing sub-3-day doorstep delivery.

---

## 2. Baseline KPI Scorecard (Summary Table)

| KPI # | Metric Name | Baseline Value | Formatted Display | Accounting Rule |
|---|---|---|---|---|
| 1 | Net Revenue | 24,620,351.40 | ₹2.46 Cr | Delivered + Shipped orders only |
| 2 | Total Orders | 9,900 | 9,900 | Distinct Order_IDs |
| 3 | Unique Customers | 2,424 | 2,424 | Distinct Customer_IDs |
| 4 | Average Order Value | 2,965.59 | ₹2,965.59 | Net Revenue / Net Orders |
| 5 | Revenue per Customer | 10,156.91 | ₹10,156.91 | Net Revenue / Unique Customers |
| 6 | Repeat Purchase Rate | 78.80% | 78.8% | Customers with ≥2 completed orders |
| 7 | Cancellation Rate | 8.34% | 8.3% | Cancelled orders / Total orders |
| 8 | Return Rate | 8.97% | 9.0% | Returned / (Delivered + Returned) |
| 9 | Average Discount | 12.51% | 12.5% | Mean promotional discount applied |
| 10 | Average Delivery Days | 3.68 days | 3.7 days | Mean fulfillment days for delivered |
| 11 | Average CSAT Rating | 4.00 / 5.0 | 4.00 / 5.0 | Mean star rating for reviewed orders |
| 12 | MoM Revenue Growth | -31.7% | -31.7% | Dec 2025 vs Nov 2025 (post-festive) |
| 13 | Top Segment Share | 38.0% | Loyal (38.0%) | Highest contributing customer cohort |
