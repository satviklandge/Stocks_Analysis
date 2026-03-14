# StockPulse — Trading Analytics Dashboard

> A production-grade stock market analytics pipeline built with Python. Historical NSE trade data is ingested via Pandas, processed through a modular analysis layer, and surfaced in a fully interactive Streamlit dashboard — enabling real-time filtering, trend visualization, sector drill-downs, and exploratory analytics without writing a single line of frontend code.

<br>

![Python](https://img.shields.io/badge/Python-3.9+-3572A5?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-e0a400?style=flat-square&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-1.26-4dabcf?style=flat-square&logo=numpy&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.x-3d6db5?style=flat-square&logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---
Dashboard
![Dashboard](assests/Screenshot2026-03-14173037.png)
![Dashboard](assests/Screenshot2026-03-14173012.png)



## Overview

StockPulse is a self-contained analytics dashboard designed for exploring historical stock trading activity. It reads a structured CSV of trade records and computes a full suite of KPIs, trend charts, and sector breakdowns — all rendered in a browser-based UI with no frontend development required.

The project demonstrates a clean separation between the data pipeline layer (Pandas transformations) and the presentation layer (Streamlit + Plotly), making it straightforward to extend, test, or plug into a live data feed.

| Attribute       | Detail                                                   |
|-----------------|----------------------------------------------------------|
| Data Source     | `stock_data_sale.csv` — NSE large-cap trades, FY 2024   |
| Analysis Type   | Exploratory Data Analysis (EDA) + KPI computation        |
| Interface       | Browser-based dashboard — runs at `localhost:8501`       |
| Visualization   | Plotly — fully interactive, zoomable charts              |
| Framework       | Streamlit — zero-frontend Python UI                      |
| Deployment      | Local or cloud (Streamlit Community Cloud, Docker)       |

---

## Dashboard Preview

> Run locally with `streamlit run Dashboard.py` to view the full interactive dashboard.

Key panels included:
- **KPI Summary Row** — Total investment, revenue, net P&L, and top-performing stock
- **Volume Chart** — Most traded stocks by total share quantity
- **Monthly Trend** — Trade value over time with area fill
- **Sector Breakdown** — Horizontal bar chart and donut chart by sector allocation
- **City Activity** — Geographic distribution of trade volume
- **Buy vs Sell Comparison** — Grouped monthly bar chart
- **Sector Drill-Down** — Filterable ranked progress bars by stock within sector
- **Quarterly Summary Table** — Buy value, sell value, and net P&L per quarter
- **Raw Data Viewer** — Collapsible full transaction log

---

## Features

**Real-time Filtering**
Filter by sector, date range, and transaction type. All charts, KPIs, and tables update instantly — no page reload required.

**Interactive Plotly Charts**
Every chart supports zoom, pan, hover tooltips, and export to PNG. Built for exploration, not just display.

**Sector Drill-Down**
Select any sector from a dropdown to see ranked stock performance within it, rendered as proportional progress bars.

**KPI Engine**
Automatically computes total investment, realized revenue, net P&L (absolute and percentage), and top performer from raw trade data on every run.

**Quarterly Aggregation**
Summarizes buy and sell activity by quarter with net P&L — useful for period-over-period comparison.

**CSV-Driven Pipeline**
No database, no API keys. Drop in any compatible trade CSV and the entire dashboard refreshes automatically.

**Power BI-Inspired Theme**
Clean light theme with Microsoft Segoe UI typography and a structured color palette — suitable for presentations and portfolio showcases.

---

## Project Structure

```
Stocks_Analysis/
├── Dashboard.py            # Streamlit application — UI layout, chart logic, KPI computation
├── style.css               # External stylesheet — Power BI-style theme and component overrides
├── stock_data_sale.csv     # Historical trade dataset (NSE large-cap, FY 2024)
├── requirements.txt        # Pinned Python dependencies
└── README.md               # Project documentation
```

### File Responsibilities

| File              | Responsibility                                                         |
|-------------------|------------------------------------------------------------------------|
| `Dashboard.py`    | Data loading, Pandas transformations, chart generation, Streamlit layout |
| `style.css`       | All visual styling — loaded dynamically by `Dashboard.py`              |
| `stock_data_sale.csv` | Source data — replace with any compatible CSV to refresh the dashboard |
| `requirements.txt` | Reproducible environment — pin versions for consistent deployments     |

---

## Getting Started

### Prerequisites

- Python 3.9 or higher
- pip (comes with Python)
- A terminal / command prompt

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/satviklandge/Stocks_Analysis.git
cd Stocks_Analysis
```

**2. (Recommended) Create a virtual environment**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Run the dashboard**

```bash
streamlit run Dashboard.py
```

**5. Open in your browser**

Streamlit launches automatically. If it does not, navigate to:

```
http://localhost:8501
```

---

## Data Schema

The dashboard expects a CSV with the following columns:

| Column              | Type     | Example          | Description                             |
|---------------------|----------|------------------|-----------------------------------------|
| `Date`              | string   | `2024-01-03`     | Trade date in `YYYY-MM-DD` format       |
| `Stock_Name`        | string   | `Reliance`       | Company / ticker name                   |
| `Sector`            | string   | `Energy`         | Sector classification                   |
| `City`              | string   | `Mumbai`         | City where the order was placed         |
| `Transaction_Type`  | string   | `Buy` / `Sell`   | Direction of the trade                  |
| `Quantity`          | integer  | `120`            | Number of shares transacted             |
| `Price_Per_Stock`   | float    | `2463.00`        | Execution price per share (INR)         |

`Total_Value` (`Quantity x Price_Per_Stock`) is computed automatically at runtime — no need to include it in the CSV.

---

## Tech Stack

| Layer         | Technology         | Purpose                                      |
|---------------|--------------------|----------------------------------------------|
| Language      | Python 3.9+        | Core application language                    |
| UI Framework  | Streamlit 1.30+    | Browser-based dashboard, no frontend code    |
| Data Layer    | Pandas 2.0+        | Data ingestion, transformation, aggregation  |
| Numerics      | NumPy 1.26+        | Array operations, axis calculations          |
| Visualization | Plotly 5.x         | Interactive, publication-grade charts        |
| Styling       | CSS3               | External stylesheet for theme and layout     |

---

## Contributing

Contributions are welcome — whether it is a bug fix, new chart type, or data pipeline improvement.

**Workflow**

```bash
# 1. Fork the repository on GitHub

# 2. Clone your fork
git clone https://github.com/your-username/Stocks_Analysis.git
cd Stocks_Analysis

# 3. Create a feature branch
git checkout -b feature/your-feature-name

# 4. Make your changes and commit
git add .
git commit -m "feat: add rolling 30-day moving average chart"

# 5. Push your branch
git push origin feature/your-feature-name

# 6. Open a Pull Request on GitHub
```
---
 
