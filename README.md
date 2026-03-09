# Stocks Analysis Dashboard

> An end-to-end stock market analysis pipeline. Historical trade data is processed through Pandas and surfaced via an interactive Streamlit dashboard — enabling real-time filtering, trend visualization, and exploratory analytics.

![Python](https://img.shields.io/badge/Python-3.9+-3572A5?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-e0a400?style=flat-square&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-1.26-4dabcf?style=flat-square&logo=numpy&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.x-3d6db5?style=flat-square&logo=plotly&logoColor=white)

---

## Overview

| Field | Detail |
|---|---|
| Data Source | `stock_data_sale.csv` |
| Analysis Type | Exploratory Data Analysis (EDA) |
| Interface | Browser-based web dashboard |
| Visualization | Plotly — interactive charts |
| Framework | Streamlit — zero-frontend Python UI |
| Core Files | 3 (Dashboard, data, dependencies) |

---

## Features

**01 — Interactive Charts**
Zoomable, pannable Plotly charts for price history, volume, and performance across any date range.

**02 — Real-time Filtering**
Filter by ticker, date range, and price range. All charts and metrics update instantly without page reload.

**03 — Exploratory Data Analysis**
Statistical breakdowns powered by Pandas — distributions, moving averages, correlations, and trend analysis.

**04 — Streamlit Dashboard**
A fully browser-based UI with no frontend code required. Runs locally with a single terminal command.

**05 — CSV-Driven Pipeline**
Drop in any compatible stock CSV to instantly refresh all charts, metrics, and analysis across the dashboard.

**06 — Publication-grade Visuals**
Clean, high-fidelity charts using Plotly — suitable for reports, presentations, and portfolio showcases.

---

## Project Structure

```
Stocks_Analysis/
  ├── Dashboard.py          # Main Streamlit application & UI logic
  ├── stock_data_sale.csv   # Historical stock market dataset
  └── requirements.txt      # Python package dependencies
```

---

## Getting Started

**1. Clone the repository**

```bash
git clone https://github.com/satviklandge/Stocks_Analysis.git
cd Stocks_Analysis
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Run the dashboard**

```bash
streamlit run Dashboard.py
```

**4. Open in your browser**

Streamlit launches automatically at `http://localhost:8501`

---

## Dependencies

```
# requirements.txt
streamlit
pandas
numpy
plotly
```

---

## Contributing

Contributions are welcome. Feel free to open an issue or submit a pull request.

1. Fork the repository
2. Create your feature branch — `git checkout -b feature/my-feature`
3. Commit your changes — `git commit -m 'Add my feature'`
4. Push to the branch — `git push origin feature/my-feature`
5. Open a Pull Request

---

*Author: [@satviklandge](https://github.com/satviklandge)*
