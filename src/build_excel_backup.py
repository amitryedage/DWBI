"""Excel BI Backup Generator for E-Commerce Customer Analytics Dashboard.

Notice Phase 5 (Deliverable 3):
Constructs a standalone Excel BI Backup workbook:
- Sheet 1: Clean_Orders_Data (Formatted analytical transaction records)
- Sheet 2: KPI_Summary (All 13 KPIs with definitions, formulas, and baseline values)
- Sheet 3: Pivot_Summaries_Charts (Pivot tables and native openpyxl Bar, Pie, and Line charts)

Saved to: data/processed/ecommerce_bi_backup.xlsx
"""

from pathlib import Path
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.chart import BarChart, PieChart, LineChart, Reference
from openpyxl.chart.series import SeriesLabel

from src.config import CLEAN_PARQUET_PATH, PROCESSED_DATA_DIR
from src.kpis import compute_all_kpis


def build_excel_backup():
    print("=" * 60)
    print("GENERATING EXCEL BI BACKUP DASHBOARD WORKBOOK")
    print("=" * 60)

    assert CLEAN_PARQUET_PATH.exists(), "Cleaned parquet data missing!"
    df = pd.read_parquet(CLEAN_PARQUET_PATH)
    kpis = compute_all_kpis(df)

    wb = Workbook()
    # Remove default sheet
    wb.remove(wb.active)

    # -------------------------------------------------------------
    # Styling Palette (Clean Professional Light Theme)
    # -------------------------------------------------------------
    header_fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    accent_fill = PatternFill(start_color="EFF6FF", end_color="EFF6FF", fill_type="solid")
    bold_font = Font(name="Calibri", size=11, bold=True, color="0F172A")
    title_font = Font(name="Calibri", size=16, bold=True, color="1E3A8A")
    sub_font = Font(name="Calibri", size=11, italic=True, color="475569")
    thin_border = Border(
        left=Side(style="thin", color="CBD5E1"),
        right=Side(style="thin", color="CBD5E1"),
        top=Side(style="thin", color="CBD5E1"),
        bottom=Side(style="thin", color="CBD5E1"),
    )

    # -------------------------------------------------------------
    # Sheet 1: KPI_Summary
    # -------------------------------------------------------------
    print("[1/3] Creating Sheet: KPI_Summary...")
    ws_kpi = wb.create_sheet(title="KPI_Summary")
    ws_kpi.views.sheetView[0].showGridLines = True

    ws_kpi["A1"] = "E-Commerce Customer Analytics: Executive KPI Summary"
    ws_kpi["A1"].font = title_font
    ws_kpi["A2"] = "Roll No. 4010 | Data Warehousing & Business Intelligence [1ADPE404] | Baseline Horizon: 2024-2025"
    ws_kpi["A2"].font = sub_font

    kpi_table = [
        ("Net Revenue", "Sum of Total_Amount for Delivered & Shipped orders", kpis["net_revenue_raw"], kpis["net_revenue_fmt"], "Headline fulfilled commercial volume"),
        ("Total Orders", "Count of distinct Order_IDs", kpis["total_orders_raw"], kpis["total_orders_fmt"], "Aggregate gross consumer purchase attempts"),
        ("Unique Customers", "Count of distinct Customer_IDs", kpis["unique_cust_raw"], kpis["unique_cust_fmt"], "Total distinct customer acquisition base"),
        ("Average Order Value (AOV)", "Net Revenue / Net Delivered & Shipped Orders", kpis["aov_raw"], kpis["aov_fmt"], "Average basket size per completed order"),
        ("Revenue per Customer", "Net Revenue / Unique Customers", kpis["rev_per_cust_raw"], kpis["rev_per_cust_fmt"], "Customer monetization & lifetime spend potential"),
        ("Repeat Purchase Rate", "(Customers with >=2 orders / Unique Customers) * 100", kpis["repeat_rate_raw"], kpis["repeat_rate_fmt"], "Customer retention & loyalty share"),
        ("Cancellation Rate", "(Cancelled orders / Total orders) * 100", kpis["cancel_rate_raw"], kpis["cancel_rate_fmt"], "Pre-dispatch operational checkout friction"),
        ("Return Rate", "Returned / (Delivered + Returned) * 100", kpis["return_rate_raw"], kpis["return_rate_fmt"], "Post-delivery merchandise dissatisfaction rate"),
        ("Average Discount %", "Mean of applied Discount_Pct", kpis["avg_discount_raw"], kpis["avg_discount_fmt"], "Promotional price markdown & margin pressure"),
        ("Average Delivery Days", "Mean of Delivery_Days for completed orders", kpis["avg_delivery_raw"], kpis["avg_delivery_fmt"], "Supply chain & logistics doorstep turnaround"),
        ("Average CSAT Rating", "Mean of submitted Customer_Rating (1-5)", kpis["avg_rating_raw"], kpis["avg_rating_fmt"], "Voice of customer post-purchase satisfaction"),
        ("MoM Revenue Growth", "(Curr Month Rev - Prior Month Rev) / Prior Month Rev", kpis["mom_growth_raw"], kpis["mom_growth_fmt"], "Month-over-month trajectory (Dec 2025 vs Nov 2025)"),
        ("Top Segment Share", "Revenue of top customer segment / Net Revenue", kpis["top_seg_pct"], kpis["top_seg_fmt"], "Customer concentration risk (Loyal Segment)"),
    ]

    headers_kpi = ["#", "KPI Metric Name", "Mathematical Formula / Logic", "Baseline Raw Value", "Formatted Display", "Business Purpose"]
    for col_idx, h in enumerate(headers_kpi, start=1):
        cell = ws_kpi.cell(row=4, column=col_idx, value=h)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center" if col_idx in [1, 4, 5] else "left", vertical="center")

    for row_idx, row_data in enumerate(kpi_table, start=5):
        ws_kpi.cell(row=row_idx, column=1, value=row_idx - 4).alignment = Alignment(horizontal="center")
        ws_kpi.cell(row=row_idx, column=2, value=row_data[0]).font = bold_font
        ws_kpi.cell(row=row_idx, column=3, value=row_data[1])
        c_raw = ws_kpi.cell(row=row_idx, column=4, value=round(row_data[2], 2) if isinstance(row_data[2], float) else row_data[2])
        c_raw.alignment = Alignment(horizontal="right")
        c_fmt = ws_kpi.cell(row=row_idx, column=5, value=row_data[3])
        c_fmt.font = bold_font
        c_fmt.alignment = Alignment(horizontal="center")
        ws_kpi.cell(row=row_idx, column=6, value=row_data[4])

        for col_idx in range(1, 7):
            ws_kpi.cell(row=row_idx, column=col_idx).border = thin_border
            if (row_idx - 4) % 2 == 1:
                ws_kpi.cell(row=row_idx, column=col_idx).fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")

    ws_kpi.column_dimensions["A"].width = 6
    ws_kpi.column_dimensions["B"].width = 28
    ws_kpi.column_dimensions["C"].width = 50
    ws_kpi.column_dimensions["D"].width = 20
    ws_kpi.column_dimensions["E"].width = 22
    ws_kpi.column_dimensions["F"].width = 45

    # -------------------------------------------------------------
    # Sheet 2: Pivot_Summaries_Charts
    # -------------------------------------------------------------
    print("[2/3] Creating Sheet: Pivot_Summaries_Charts with native Excel charts...")
    ws_charts = wb.create_sheet(title="Pivot_Summaries_Charts")
    ws_charts.views.sheetView[0].showGridLines = True

    ws_charts["A1"] = "Executive BI Pivot Tables & Visualizations"
    ws_charts["A1"].font = title_font

    # --- Pivot 1: Category Net Revenue (Rows 4 to 12) ---
    ws_charts["A3"] = "Product Category"
    ws_charts["B3"] = "Net Revenue (INR)"
    ws_charts["A3"].fill = header_fill
    ws_charts["B3"].fill = header_fill
    ws_charts["A3"].font = header_font
    ws_charts["B3"].font = header_font

    net_df = df[df["Net_Flag"] == True]
    cat_summary = net_df.groupby("Product_Category")["Total_Amount"].sum().reset_index().sort_values("Total_Amount", ascending=False)
    for r_idx, (_, row) in enumerate(cat_summary.iterrows(), start=4):
        ws_charts.cell(row=r_idx, column=1, value=row["Product_Category"]).border = thin_border
        c = ws_charts.cell(row=r_idx, column=2, value=round(row["Total_Amount"], 2))
        c.number_format = "#,##0"
        c.border = thin_border

    # Add Bar Chart for Category
    chart_bar = BarChart()
    chart_bar.type = "col"
    chart_bar.style = 10
    chart_bar.title = "Net Revenue by Product Category"
    chart_bar.y_axis.title = "Revenue (INR)"
    chart_bar.x_axis.title = "Category"
    data_ref = Reference(ws_charts, min_col=2, min_row=3, max_row=3 + len(cat_summary))
    cats_ref = Reference(ws_charts, min_col=1, min_row=4, max_row=3 + len(cat_summary))
    chart_bar.add_data(data_ref, titles_from_data=True)
    chart_bar.set_categories(cats_ref)
    chart_bar.legend = None
    chart_bar.width = 16
    chart_bar.height = 10
    ws_charts.add_chart(chart_bar, "D3")

    # --- Pivot 2: Order Status Share (Rows 15 to 19) ---
    ws_charts["A15"] = "Order Status"
    ws_charts["B15"] = "Order Count"
    ws_charts["A15"].fill = header_fill
    ws_charts["B15"].fill = header_fill
    ws_charts["A15"].font = header_font
    ws_charts["B15"].font = header_font

    status_summary = df["Order_Status"].value_counts().reset_index()
    status_summary.columns = ["Order_Status", "Count"]
    for r_idx, (_, row) in enumerate(status_summary.iterrows(), start=16):
        ws_charts.cell(row=r_idx, column=1, value=row["Order_Status"]).border = thin_border
        c = ws_charts.cell(row=r_idx, column=2, value=int(row["Count"]))
        c.number_format = "#,##0"
        c.border = thin_border

    # Add Pie Chart for Order Status
    chart_pie = PieChart()
    chart_pie.title = "Order Fulfillment Breakdown"
    data_ref_pie = Reference(ws_charts, min_col=2, min_row=15, max_row=15 + len(status_summary))
    cats_ref_pie = Reference(ws_charts, min_col=1, min_row=16, max_row=15 + len(status_summary))
    chart_pie.add_data(data_ref_pie, titles_from_data=True)
    chart_pie.set_categories(cats_ref_pie)
    chart_pie.width = 14
    chart_pie.height = 9
    ws_charts.add_chart(chart_pie, "D18")

    # --- Pivot 3: Monthly Net Revenue Trend (Rows 22 to 46) ---
    ws_charts["A22"] = "Month (YYYY-MM)"
    ws_charts["B22"] = "Net Revenue (INR)"
    ws_charts["A22"].fill = header_fill
    ws_charts["B22"].fill = header_fill
    ws_charts["A22"].font = header_font
    ws_charts["B22"].font = header_font

    monthly_summary = net_df.groupby("Year_Month")["Total_Amount"].sum().reset_index().sort_values("Year_Month")
    for r_idx, (_, row) in enumerate(monthly_summary.iterrows(), start=23):
        ws_charts.cell(row=r_idx, column=1, value=row["Year_Month"]).border = thin_border
        c = ws_charts.cell(row=r_idx, column=2, value=round(row["Total_Amount"], 2))
        c.number_format = "#,##0"
        c.border = thin_border

    # Add Line Chart for Trend
    chart_line = LineChart()
    chart_line.title = "Monthly Net Revenue Trend (2024-2025)"
    chart_line.style = 13
    chart_line.y_axis.title = "Net Revenue (INR)"
    chart_line.x_axis.title = "Month"
    data_ref_line = Reference(ws_charts, min_col=2, min_row=22, max_row=22 + len(monthly_summary))
    cats_ref_line = Reference(ws_charts, min_col=1, min_row=23, max_row=22 + len(monthly_summary))
    chart_line.add_data(data_ref_line, titles_from_data=True)
    chart_line.set_categories(cats_ref_line)
    chart_line.legend = None
    chart_line.width = 18
    chart_line.height = 10
    ws_charts.add_chart(chart_line, "D32")

    ws_charts.column_dimensions["A"].width = 24
    ws_charts.column_dimensions["B"].width = 22

    # -------------------------------------------------------------
    # Sheet 3: Clean_Orders_Data (Formatted Tabular Data)
    # -------------------------------------------------------------
    print("[3/3] Exporting Clean_Orders_Data table (9,900 rows)...")
    ws_data = wb.create_sheet(title="Clean_Orders_Data")
    ws_data.views.sheetView[0].showGridLines = True

    # Write dataframe rows
    for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=True), start=1):
        ws_data.append(row)
        if r_idx == 1:
            for c_idx in range(1, len(row) + 1):
                cell = ws_data.cell(row=1, column=c_idx)
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = Alignment(horizontal="center", vertical="center")

    # Set column widths
    for col in ws_data.columns:
        max_len = max(len(str(cell.value or '')) for cell in col[:20])
        col_letter = col[0].column_letter
        ws_data.column_dimensions[col_letter].width = max(max_len + 3, 12)

    # Save final workbook
    output_path = PROCESSED_DATA_DIR / "ecommerce_bi_backup.xlsx"
    wb.save(output_path)
    file_size_mb = output_path.stat().st_size / (1024 * 1024)
    print("=" * 60)
    print(f"EXCEL BI BACKUP CREATED SUCCESSFULLY: {output_path}")
    print(f"File Size: {file_size_mb:.2f} MB | Sheets: {wb.sheetnames}")
    print("=" * 60)
    return output_path


if __name__ == "__main__":
    build_excel_backup()
