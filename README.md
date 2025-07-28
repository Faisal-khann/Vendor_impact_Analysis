# 📦 Vendor Performance Analysis Project

Effective inventory and sales management is crucial for optimizing profitability in the retail and wholesale sectors. This project aims to help businesses identify inefficiencies in pricing, vendor performance, and inventory turnover to enhance decision-making and overall profitability.

---

## Project Workflow

<img width="1240" height="685" alt="Image" src="https://github.com/user-attachments/assets/98b9225b-ef6b-43f1-b708-2ee15e2079a8" />

## Business Problem

Companies often face losses due to poor inventory practices, inefficient pricing strategies, and vendor over-dependence. This analysis aims to:

- Identify underperforming brands needing promotional or pricing adjustments.
- Determine top vendors contributing to sales and gross profit.
- Analyze the effect of bulk purchasing on unit cost.
- Assess inventory turnover to improve efficiency and reduce holding costs.
- Investigate profitability variance between high- and low-performing vendors

## Tools & Technologies

| Tool        | Purpose                         |
|-------------|----------------------------------|
| **Python**  | Data analysis & scripting        |
| **Pandas**  | Data manipulation                |
| **SQL**     | Data extraction from SQLite      |
| **Power BI**| Dashboard creation               |
| **Jupyter** | EDA & visualization              |
| **Matplotlib/Seaborn** | Visual analytics     |

---

## Database Connection

To run the analysis, establish a connection to the SQLite database:

```python
from sqlalchemy import create_engine
import pandas as pd
import sqlite3

# Create a SQLAlchemy engine to connect to the SQLite database named 'inventory.db'
engine = create_engine('sqlite:///inventory.db')

# Connect to the SQLite database file
conn = sqlite3.connect('inventory.db')

# Checking tables present in the database
tables = pd.read_sql_query(
    "SELECT name FROM sqlite_master
     WHERE type='table' ORDER BY name ASC", conn
)
tables


```

## Data Aggregation using SQL (Final Query)
The query below creates the final `vendor_sales_summary` by joining purchase, sales, and freight data using Common Table Expressions (CTEs):

```python
vendor_sales_summary = pd.read_sql_query("""
WITH FreightSummary AS (
    SELECT
        VendorNumber, 
        SUM(Freight) AS FreightCost 
    FROM vendor_invoice
    GROUP BY VendorNumber
), 
PurchaseSummary AS (
    SELECT
        p.VendorNumber,
        p.VendorName,
        p.Brand, 
        p.Description, 
        p.PurchasePrice, 
        pp.Volume, 
        pp.Price AS ActualPrice,
        SUM(p.Quantity) AS TotalPurchaseQuantity,
        SUM(p.Dollars) AS TotalPurchaseDollars
    FROM purchases p
    JOIN purchase_prices pp
        ON p.Brand = pp.Brand
    WHERE p.PurchasePrice > 0
    GROUP BY 
        p.VendorNumber, p.VendorName, p.Brand, p.Description, p.PurchasePrice, pp.Price, pp.Volume
),
SalesSummary AS (
    SELECT 
        VendorNo, 
        Brand, 
        SUM(SalesDollars) AS TotalSalesDollars,
        SUM(SalesPrice) AS TotalSalesPrice,
        SUM(SalesQuantity) AS TotalSalesQuantity,
        SUM(ExciseTax) AS TotalExciseTax
    FROM sales
    GROUP BY VendorNo, Brand
)
SELECT 
    ps.VendorNumber,
    ps.VendorName, 
    ps.Brand,
    ps.Description, 
    ps.PurchasePrice, 
    ps.ActualPrice,
    ps.Volume, 
    ps.TotalPurchaseQuantity, 
    ps.TotalPurchaseDollars,
    ss.TotalSalesQuantity,
    ss.TotalSalesDollars,
    ss.TotalSalesPrice,
    ss.TotalExciseTax,
    fs.FreightCost
FROM PurchaseSummary ps 
LEFT JOIN SalesSummary ss
    ON ps.VendorNumber = ss.VendorNo
    AND ps.Brand = ss.Brand
LEFT JOIN FreightSummary fs
    ON ps.VendorNumber = fs.VendorNumber
ORDER BY ps.TotalPurchaseDollars DESC
""", conn)

```


## 📂 Folder Structure

```
Vendor_Performance_Analysis/
│
├── data/
│   └── inventory.db                  # SQLite database
│
├── sql/                               # SQL scripts for data cleaning and aggregation
│
├── notebooks/
│   └── Vendor_Performance_Analysis.ipynb  # Main notebook
│
│
├── logs/
│   └── ingestion.log                 # Logs for ETL operations
│
├── scripts/
│   └── ingest_to_db.py              # Save aggregated table to DB
│
├── powerbi/
│   └── dashboard.pbix               # Power BI dashboard file
│
├── report/
│   └── final_report.pdf             # Business summary
│
└── README.md                        # Project documentation
```

---


## Data Pipeline Overview

```mermaid
graph TD;
    A[Define Business Problem] --> B[Explore DB with SQL];
    B --> C[Clean & Merge Tables];
    C --> D[Create Aggregated Table];
    D --> E[Save to SQLite DB];
    D --> F[Load in Jupyter];
    F --> G[Perform EDA];
    G --> H[Create Power BI Dashboard];
    H --> I[Report Insights];
```

---

## Power BI Dashboard Preview

Below is a preview of the Power BI dashboard showing key vendor KPIs:
<img width="1071" height="604" alt="Image" src="https://github.com/user-attachments/assets/b2b05186-b7ff-4070-803b-2ae922487cec" />
<img width="1070" height="603" alt="Image" src="https://github.com/user-attachments/assets/e57c3d82-f87f-44fd-829f-ca53793f5edd" />

> 📁 File: `powerbi/Inventory_Management.pbix`

---

## Report Summary

The final report contains:
- Project Goals
- Analysis Methodology
- Key Insights
- Recommendations

📁 File: `report/final_report.pdf`

---

## Outcomes & Insights

- Identified top and low-performing vendors based on delivery time and rating
- Highlighted cost-effectiveness of certain vendors
- Suggested potential areas for renegotiation and vendor replacement

  <img width="1536" height="1024" alt="Image" src="https://github.com/user-attachments/assets/695dcaf9-b704-4dd3-8258-90b0ab61dc30" />

---

## 📎 Resources

- Full Jupyter Notebook: [`Vendor_Performance_Analysis.ipynb`](notebooks/Vendor_Performance_Analysis.ipynb)

## 🙋‍♂️ Author

**Faisal Khan**  
*Data Analyst | Python | SQL | Power BI*

📧 Contact: *thisside.faisalkhan@example.com*  
🔗 GitHub: [github.com/yourusername](https://github.com/Faisal-khann)
