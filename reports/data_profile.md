# Data Profile Report: Raw E-Commerce Transactional Dataset

**Source:** `data/raw/ecommerce_data.xlsx`  
**Course:** Data Warehousing & Business Intelligence [1ADPE404] | Roll No. 4010  
**Generated:** Automatically profiled from raw dataset  

---

## 1. Executive Summary

- **Sheets in Workbook:** Orders_Data, Data_Dictionary, About
- **Raw Shape:** 10,000 rows × 20 columns
- **Exact Duplicate Rows:** 100 rows
- **Unique Order IDs:** 9,900 (Duplicate IDs: 100)
- **Unique Customers:** 2,424
- **Date Range:** 2024-01-01 to 2025-12-31 (24 months)
- **Total Amount Formula Check:** Max discrepancy = 0.0000 INR (0 discrepancies > ₹0.01)

---

## 2. Column-by-Column Missing Value & Type Audit

| Column | Data Type | Non-Null Count | Missing Count | Missing % | Notes |
|---|---|---|---|---|---|
| `Order_ID` | `object` | 10,000 | 0 | 0.0% | Clean |
| `Order_Date` | `datetime64[ns]` | 10,000 | 0 | 0.0% | Clean |
| `Customer_ID` | `object` | 10,000 | 0 | 0.0% | Clean |
| `Customer_Name` | `object` | 10,000 | 0 | 0.0% | Clean |
| `Gender` | `object` | 9,857 | 143 | 1.43% | Requires Phase 2 imputation |
| `Age` | `float64` | 9,814 | 186 | 1.86% | Requires Phase 2 imputation |
| `City` | `object` | 9,902 | 98 | 0.98% | Requires Phase 2 imputation |
| `State` | `object` | 10,000 | 0 | 0.0% | Clean |
| `Customer_Segment` | `object` | 10,000 | 0 | 0.0% | Clean |
| `Product_Category` | `object` | 10,000 | 0 | 0.0% | Clean |
| `Product_Name` | `object` | 10,000 | 0 | 0.0% | Clean |
| `Unit_Price` | `int64` | 10,000 | 0 | 0.0% | Clean |
| `Quantity` | `int64` | 10,000 | 0 | 0.0% | Clean |
| `Discount_Pct` | `int64` | 10,000 | 0 | 0.0% | Clean |
| `Total_Amount` | `float64` | 10,000 | 0 | 0.0% | Clean |
| `Payment_Method` | `object` | 9,912 | 88 | 0.88% | Requires Phase 2 imputation |
| `Order_Status` | `object` | 10,000 | 0 | 0.0% | Clean |
| `Delivery_Days` | `float64` | 8,729 | 1,271 | 12.71% | Legitimate business blanks |
| `Customer_Rating` | `float64` | 6,139 | 3,861 | 38.61% | Legitimate business blanks |
| `Device_Type` | `object` | 10,000 | 0 | 0.0% | Clean |

---

## 3. Numerical Summary Statistics

| Column | Count | Mean | Median | Std Dev | Min | 25% | 75% | Max |
|---|---|---|---|---|---|---|---|---|
| `Age` | 9,814 | 32.27 | 32.00 | 8.43 | 18.00 | 26.00 | 38.00 | 64.00 |
| `Unit_Price` | 10,000 | 2240.70 | 1444.00 | 3389.89 | 185.00 | 787.00 | 2417.25 | 20511.00 |
| `Quantity` | 10,000 | 1.75 | 1.00 | 1.10 | 1.00 | 1.00 | 2.00 | 5.00 |
| `Discount_Pct` | 10,000 | 12.51 | 10.00 | 9.52 | 0.00 | 5.00 | 20.00 | 40.00 |
| `Total_Amount` | 10,000 | 2949.08 | 1851.15 | 3465.13 | 128.40 | 921.60 | 3400.25 | 20498.00 |
| `Delivery_Days` | 8,729 | 3.68 | 4.00 | 1.78 | 1.00 | 2.00 | 5.00 | 11.00 |
| `Customer_Rating` | 6,139 | 4.00 | 4.00 | 0.86 | 1.00 | 3.00 | 5.00 | 5.00 |

---

## 4. Categorical Attribute Value Counts

### `Customer_Segment` Breakdown

| Category Value | Frequency | Share % |
|---|---|---|
| Loyal | 3,788 | 37.88% |
| Regular | 2,796 | 27.96% |
| VIP | 2,252 | 22.52% |
| New | 1,164 | 11.64% |

### `Product_Category` Breakdown

| Category Value | Frequency | Share % |
|---|---|---|
| Electronics | 2,190 | 21.90% |
| Fashion | 1,978 | 19.78% |
| Home & Kitchen | 1,427 | 14.27% |
| Beauty & Personal Care | 1,139 | 11.39% |
| Grocery & Gourmet | 940 | 9.40% |
| Sports & Fitness | 862 | 8.62% |
| Toys & Baby | 771 | 7.71% |
| Books & Stationery | 693 | 6.93% |

### `Order_Status` Breakdown

| Category Value | Frequency | Share % |
|---|---|---|
| Delivered | 7,949 | 79.49% |
| Cancelled | 834 | 8.34% |
| Returned | 780 | 7.80% |
| Shipped | 437 | 4.37% |

### `Payment_Method` Breakdown

| Category Value | Frequency | Share % |
|---|---|---|
| UPI | 3,571 | 35.71% |
| Cash on Delivery | 2,030 | 20.30% |
| Credit Card | 1,649 | 16.49% |
| Debit Card | 1,394 | 13.94% |
| Net Banking | 711 | 7.11% |
| Wallet | 557 | 5.57% |
| *(Missing / Null)* | 88 | 0.88% |

### `Device_Type` Breakdown

| Category Value | Frequency | Share % |
|---|---|---|
| Mobile App | 5,416 | 54.16% |
| Desktop | 2,160 | 21.60% |
| Mobile Web | 2,078 | 20.78% |
| Tablet | 346 | 3.46% |

### `Gender` Breakdown

| Category Value | Frequency | Share % |
|---|---|---|
| Male | 5,177 | 51.77% |
| Female | 4,680 | 46.80% |
| *(Missing / Null)* | 143 | 1.43% |

---

## 5. Key Findings for Phase 2 Cleaning

1. **Deduplication:** Exactly 100 duplicate rows need to be purged, leaving exactly 9,900 valid analytical rows.
2. **Age Imputation:** Median age must be computed and filled into missing values, accompanied by an `Age_Imputed` boolean flag.
3. **Unknown Imputation:** `Gender`, `City`, and `Payment_Method` should be imputed as `'Unknown'` to prevent artificial bias.
4. **Fulfillment Blanks:** Blank `Delivery_Days` must remain null for `Cancelled` and `Shipped` orders.
5. **Review Exclusions:** Null `Customer_Rating` entries must be excluded from average calculations without defaulting to zero.
