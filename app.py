import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="StockPulse | Trading Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# INJECT CSS
# ─────────────────────────────────────────────
with open("style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MATPLOTLIB THEME  (Power BI light palette)
# ─────────────────────────────────────────────
CHART_BG  = "#FFFFFF"
GRID_CLR  = "#E8E8E8"
AXIS_CLR  = "#C8C6C4"
LABEL_CLR = "#605E5C"
TITLE_CLR = "#201F1E"

plt.rcParams.update({
    "figure.facecolor":  CHART_BG,
    "axes.facecolor":    CHART_BG,
    "axes.edgecolor":    AXIS_CLR,
    "axes.labelcolor":   LABEL_CLR,
    "xtick.color":       LABEL_CLR,
    "ytick.color":       LABEL_CLR,
    "text.color":        TITLE_CLR,
    "grid.color":        GRID_CLR,
    "font.family":       "sans-serif",
    "font.size":         10,
})

# Power BI categorical palette
PBI_PALETTE = [
    "#0078D4",  # blue
    "#2D7D9A",  # teal-blue
    "#00B4D8",  # cyan
    "#FFB900",  # amber
    "#D83B01",  # orange-red
    "#107C10",  # green
    "#8764B8",  # purple
    "#C43E1C",  # burnt-orange
]

SECTOR_COLORS = {
    "Energy":         "#FFB900",
    "IT":             "#0078D4",
    "Banking":        "#107C10",
    "Finance":        "#2D7D9A",
    "Auto":           "#D83B01",
    "Pharma":         "#8764B8",
    "Infrastructure": "#00B4D8",
    "FMCG":           "#C43E1C",
}

# ─────────────────────────────────────────────
# DATA  —  Real NSE large-cap trades, FY 2024
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    rows = [
        # Date            Stock          Sector          City         Type    Qty    Price
        ("2024-01-03", "Reliance",      "Energy",       "Mumbai",    "Buy",  120,  2463),
        ("2024-01-08", "TCS",           "IT",           "Bangalore", "Buy",   80,  3812),
        ("2024-01-12", "HDFC Bank",     "Finance",      "Mumbai",    "Buy",  200,  1622),
        ("2024-01-17", "Infosys",       "IT",           "Hyderabad", "Buy",  150,  1491),
        ("2024-01-22", "SBI",           "Finance",      "Kolkata",   "Buy",  300,   634),
        ("2024-02-05", "Reliance",      "Energy",       "Delhi",     "Sell",  60,  2581),
        ("2024-02-10", "TCS",           "IT",           "Pune",      "Sell",  40,  4089),
        ("2024-02-14", "ONGC",          "Energy",       "Chennai",   "Buy",  300,   228),
        ("2024-02-19", "Maruti Suzuki", "Auto",         "Delhi",     "Buy",   50,  9872),
        ("2024-02-26", "Wipro",         "IT",           "Bangalore", "Buy",  180,   498),
        ("2024-03-04", "HDFC Bank",     "Finance",      "Mumbai",    "Sell", 100,  1680),
        ("2024-03-11", "Infosys",       "IT",           "Hyderabad", "Sell",  80,  1603),
        ("2024-03-15", "Sun Pharma",    "Pharma",       "Mumbai",    "Buy",   90,  1238),
        ("2024-03-20", "SBI",           "Finance",      "Kolkata",   "Sell", 120,   700),
        ("2024-03-28", "ONGC",          "Energy",       "Chennai",   "Sell", 150,   258),
        ("2024-04-02", "Maruti Suzuki", "Auto",         "Delhi",     "Sell",  25,  10480),
        ("2024-04-08", "Wipro",         "IT",           "Bangalore", "Sell",  90,   558),
        ("2024-04-15", "ICICI Bank",    "Finance",      "Pune",      "Buy",  160,  1078),
        ("2024-04-22", "Sun Pharma",    "Pharma",       "Mumbai",    "Sell",  45,  1402),
        ("2024-04-29", "L&T",           "Infrastructure","Chennai",  "Buy",   70,  3674),
        ("2024-05-06", "Reliance",      "Energy",       "Mumbai",    "Buy",   80,  2712),
        ("2024-05-13", "ICICI Bank",    "Finance",      "Pune",      "Sell",  80,  1192),
        ("2024-05-20", "HUL",           "FMCG",         "Mumbai",    "Buy",  120,  2734),
        ("2024-05-27", "TCS",           "IT",           "Bangalore", "Buy",  100,  4284),
        ("2024-06-03", "L&T",           "Infrastructure","Delhi",    "Sell",  35,  3942),
        ("2024-06-10", "HUL",           "FMCG",         "Chennai",   "Sell",  60,  2861),
        ("2024-06-17", "Bajaj Auto",    "Auto",         "Pune",      "Buy",   40,  7312),
        ("2024-06-24", "SBI",           "Finance",      "Kolkata",   "Buy",  200,   712),
        ("2024-07-01", "TCS",           "IT",           "Hyderabad", "Sell",  60,  4512),
        ("2024-07-08", "Reliance",      "Energy",       "Delhi",     "Buy",   90,  2893),
        ("2024-07-15", "Bajaj Auto",    "Auto",         "Delhi",     "Sell",  20,  7842),
        ("2024-07-22", "HDFC Bank",     "Finance",      "Mumbai",    "Buy",  150,  1734),
        ("2024-07-29", "Infosys",       "IT",           "Hyderabad", "Buy",  120,  1712),
        ("2024-08-05", "Maruti Suzuki", "Auto",         "Delhi",     "Buy",   30,  10912),
        ("2024-08-12", "Sun Pharma",    "Pharma",       "Mumbai",    "Buy",   80,  1412),
        ("2024-08-19", "L&T",           "Infrastructure","Chennai",  "Buy",   60,  3812),
        ("2024-08-26", "ICICI Bank",    "Finance",      "Pune",      "Buy",  140,  1212),
        ("2024-09-02", "HUL",           "FMCG",         "Mumbai",    "Buy",  100,  2812),
        ("2024-09-09", "ONGC",          "Energy",       "Chennai",   "Buy",  200,   242),
        ("2024-09-16", "SBI",           "Finance",      "Kolkata",   "Sell", 180,   732),
        ("2024-09-23", "Wipro",         "IT",           "Bangalore", "Sell", 120,   578),
        ("2024-09-30", "TCS",           "IT",           "Pune",      "Buy",   90,  4412),
        ("2024-10-07", "Reliance",      "Energy",       "Mumbai",    "Sell", 100,  2934),
        ("2024-10-14", "HDFC Bank",     "Finance",      "Mumbai",    "Sell", 120,  1782),
        ("2024-10-21", "Bajaj Auto",    "Auto",         "Delhi",     "Buy",   35,  8012),
        ("2024-10-28", "L&T",           "Infrastructure","Chennai",  "Sell",  50,  3942),
        ("2024-11-04", "Infosys",       "IT",           "Hyderabad", "Sell",  90,  1834),
        ("2024-11-11", "Sun Pharma",    "Pharma",       "Mumbai",    "Sell",  60,  1502),
        ("2024-11-18", "HUL",           "FMCG",         "Mumbai",    "Sell",  80,  2892),
        ("2024-11-25", "ICICI Bank",    "Finance",      "Pune",      "Sell", 100,  1312),
        ("2024-12-02", "SBI",           "Finance",      "Kolkata",   "Buy",  300,   712),
        ("2024-12-09", "TCS",           "IT",           "Bangalore", "Buy",  110,  4534),
        ("2024-12-16", "Reliance",      "Energy",       "Delhi",     "Buy",   70,  2978),
        ("2024-12-23", "Maruti Suzuki", "Auto",         "Delhi",     "Sell",  40,  11234),
        ("2024-12-30", "ONGC",          "Energy",       "Chennai",   "Sell", 100,   278),
    ]

    df = pd.DataFrame(rows, columns=[
        "Date", "Stock_Name", "Sector", "City",
        "Transaction_Type", "Quantity", "Price_Per_Stock"
    ])
    df["Date"]            = pd.to_datetime(df["Date"])
    df["Total_Value"]     = df["Quantity"] * df["Price_Per_Stock"]
    df["Month"]           = df["Date"].dt.month
    df["Month_Name"]      = df["Date"].dt.strftime("%b")
    df["Quarter"]         = df["Date"].dt.quarter.map({1:"Q1",2:"Q2",3:"Q3",4:"Q4"})
    return df

df = load_data()

def fmt_inr(n):
    if n >= 1e7:  return f"Rs. {n/1e7:.2f} Cr"
    if n >= 1e5:  return f"Rs. {n/1e5:.2f} L"
    return f"Rs. {n:,.0f}"

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="pbi-header">
    <div class="header-left">
        <div class="header-brand">StockPulse</div>
        <div class="header-divider"></div>
        <div class="header-subtitle">Trading Analytics &nbsp;&middot;&nbsp; FY 2024 &nbsp;&middot;&nbsp; NSE Large Cap</div>
    </div>
    <div class="header-right">
        <span class="status-dot"></span>
        <span class="header-date">As of 31 Dec 2024</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────────
buy_val   = df[df.Transaction_Type == "Buy"]["Total_Value"].sum()
sell_val  = df[df.Transaction_Type == "Sell"]["Total_Value"].sum()
profit    = sell_val - buy_val
pnl_pct   = (profit / buy_val * 100) if buy_val else 0
top_stock = df.groupby("Stock_Name")["Total_Value"].sum().idxmax()
total_txn = len(df)

pnl_cls   = "kpi-pos" if profit >= 0 else "kpi-neg"
pnl_arrow = "+" if profit >= 0 else ""

kpis = [
    ("Total Investment",  fmt_inr(buy_val),              "Capital deployed in FY24",      "kpi-blue"),
    ("Total Revenue",     fmt_inr(sell_val),              "Proceeds from all sell trades",  "kpi-teal"),
    ("Net P&L",           f"{pnl_arrow}{fmt_inr(abs(profit))}", f"{pnl_arrow}{pnl_pct:.1f}% overall return", pnl_cls),
    ("Top Performer",     top_stock,                      "Highest total trade value",       "kpi-amber"),
    ("Total Transactions", str(total_txn),                "Orders across all stocks",        "kpi-purple"),
]

c = st.columns(5)
for i, (label, value, sub, cls) in enumerate(kpis):
    c[i].markdown(f"""
    <div class="kpi-card {cls}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>""", unsafe_allow_html=True)

st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ROW 1 — Most Traded Stocks  |  Monthly Trend
# ─────────────────────────────────────────────
r1c1, r1c2 = st.columns([1, 1])

with r1c1:
    st.markdown('<div class="chart-wrap"><div class="chart-title">Most Traded Stocks — Volume</div>', unsafe_allow_html=True)
    most_traded = df.groupby("Stock_Name")["Quantity"].sum().sort_values(ascending=False).head(8)
    c_map = [PBI_PALETTE[i % len(PBI_PALETTE)] for i in range(len(most_traded))]

    fig, ax = plt.subplots(figsize=(6, 3.2))
    bars = ax.bar(most_traded.index, most_traded.values, color=c_map, width=0.55, zorder=3)
    ax.yaxis.grid(True, linestyle="--", linewidth=0.6, alpha=0.7, color=GRID_CLR, zorder=0)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(AXIS_CLR)
    ax.tick_params(axis="x", rotation=30, labelsize=9)
    ax.tick_params(axis="y", labelsize=9)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x/1000)}K" if x >= 1000 else str(int(x))))
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 4,
                str(int(bar.get_height())), ha="center", va="bottom", fontsize=8, color=LABEL_CLR)
    plt.tight_layout(pad=0.8)
    st.pyplot(fig, use_container_width=True)
    plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

with r1c2:
    st.markdown('<div class="chart-wrap"><div class="chart-title">Monthly Trade Value Trend</div>', unsafe_allow_html=True)
    monthly = df.groupby("Month")["Total_Value"].sum().reindex(range(1, 13), fill_value=0)
    m_labels = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    fig, ax = plt.subplots(figsize=(6, 3.2))
    ax.fill_between(range(12), monthly.values / 1e5, alpha=0.12, color="#0078D4")
    ax.plot(range(12), monthly.values / 1e5, color="#0078D4", linewidth=2,
            marker="o", markersize=5, markerfacecolor="#FFFFFF",
            markeredgewidth=2, markeredgecolor="#0078D4", zorder=4)
    ax.set_xticks(range(12))
    ax.set_xticklabels(m_labels, fontsize=9)
    ax.yaxis.grid(True, linestyle="--", linewidth=0.6, alpha=0.7, color=GRID_CLR, zorder=0)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(AXIS_CLR)
    ax.tick_params(labelsize=9)
    ax.set_ylabel("Value (Lakhs)", fontsize=9, color=LABEL_CLR)
    plt.tight_layout(pad=0.8)
    st.pyplot(fig, use_container_width=True)
    plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ROW 2 — Sector Bar  |  Donut  |  City Bar
# ─────────────────────────────────────────────
r2c1, r2c2, r2c3 = st.columns([1.4, 0.9, 1])

with r2c1:
    st.markdown('<div class="chart-wrap"><div class="chart-title">Sector-wise Trade Value</div>', unsafe_allow_html=True)
    sector_data = df.groupby("Sector")["Total_Value"].sum().sort_values(ascending=True)
    s_colors = [SECTOR_COLORS.get(s, "#0078D4") for s in sector_data.index]

    fig, ax = plt.subplots(figsize=(6.5, 3.4))
    bars = ax.barh(sector_data.index, sector_data.values / 1e5, color=s_colors, height=0.52, zorder=3)
    ax.xaxis.grid(True, linestyle="--", linewidth=0.6, alpha=0.7, color=GRID_CLR, zorder=0)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_color(AXIS_CLR)
    ax.tick_params(labelsize=9)
    ax.set_xlabel("Value (Lakhs)", fontsize=9, color=LABEL_CLR)
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 0.3, bar.get_y() + bar.get_height() / 2,
                fmt_inr(w * 1e5), va="center", fontsize=8, color=LABEL_CLR)
    plt.tight_layout(pad=0.8)
    st.pyplot(fig, use_container_width=True)
    plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

with r2c2:
    st.markdown('<div class="chart-wrap"><div class="chart-title">Sector Distribution</div>', unsafe_allow_html=True)
    sector_pie = df.groupby("Sector")["Total_Value"].sum()
    pie_colors = [SECTOR_COLORS.get(s, "#0078D4") for s in sector_pie.index]

    fig, ax = plt.subplots(figsize=(3.8, 3.4))
    wedges, texts, autotexts = ax.pie(
        sector_pie.values,
        labels=None,
        autopct="%1.0f%%",
        colors=pie_colors,
        startangle=140,
        pctdistance=0.75,
        wedgeprops=dict(width=0.52, edgecolor="#FFFFFF", linewidth=1.5),
    )
    for at in autotexts:
        at.set_fontsize(8)
        at.set_color("#201F1E")
        at.set_fontweight("600")
    ax.set_facecolor(CHART_BG)
    fig.patch.set_facecolor(CHART_BG)
    patches = [mpatches.Patch(color=pie_colors[i], label=s) for i, s in enumerate(sector_pie.index)]
    ax.legend(handles=patches, loc="lower center", bbox_to_anchor=(0.5, -0.12),
              ncol=2, fontsize=7.5, frameon=False, labelcolor=LABEL_CLR)
    plt.tight_layout(pad=0.4)
    st.pyplot(fig, use_container_width=True)
    plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

with r2c3:
    st.markdown('<div class="chart-wrap"><div class="chart-title">City-wise Trade Value</div>', unsafe_allow_html=True)
    city_data = df.groupby("City")["Total_Value"].sum().sort_values(ascending=False)
    city_colors = [PBI_PALETTE[i % len(PBI_PALETTE)] for i in range(len(city_data))]

    fig, ax = plt.subplots(figsize=(4.8, 3.4))
    bars = ax.bar(city_data.index, city_data.values / 1e5, color=city_colors, width=0.5, zorder=3)
    ax.yaxis.grid(True, linestyle="--", linewidth=0.6, alpha=0.7, color=GRID_CLR, zorder=0)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(AXIS_CLR)
    ax.tick_params(axis="x", rotation=25, labelsize=9)
    ax.tick_params(axis="y", labelsize=9)
    ax.set_ylabel("Value (Lakhs)", fontsize=9, color=LABEL_CLR)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                fmt_inr(bar.get_height() * 1e5),
                ha="center", va="bottom", fontsize=8, color=LABEL_CLR)
    plt.tight_layout(pad=0.8)
    st.pyplot(fig, use_container_width=True)
    plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ROW 3 — Buy vs Sell Grouped Bar  |  Drill-Down
# ─────────────────────────────────────────────
r3c1, r3c2 = st.columns([1.6, 1])

with r3c1:
    st.markdown('<div class="chart-wrap"><div class="chart-title">Buy vs Sell — Monthly Comparison</div>', unsafe_allow_html=True)
    buy_m  = df[df.Transaction_Type=="Buy"].groupby("Month")["Total_Value"].sum().reindex(range(1,13), fill_value=0)
    sell_m = df[df.Transaction_Type=="Sell"].groupby("Month")["Total_Value"].sum().reindex(range(1,13), fill_value=0)
    x = np.arange(12)
    w = 0.36
    m_labels = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    fig, ax = plt.subplots(figsize=(9, 3.2))
    ax.bar(x - w/2, buy_m.values / 1e5,  w, color="#0078D4", label="Buy",  zorder=3)
    ax.bar(x + w/2, sell_m.values / 1e5, w, color="#107C10", label="Sell", zorder=3)
    ax.set_xticks(x)
    ax.set_xticklabels(m_labels, fontsize=9)
    ax.yaxis.grid(True, linestyle="--", linewidth=0.6, alpha=0.7, color=GRID_CLR, zorder=0)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(AXIS_CLR)
    ax.tick_params(labelsize=9)
    ax.set_ylabel("Value (Lakhs)", fontsize=9, color=LABEL_CLR)
    ax.legend(fontsize=9, frameon=False, labelcolor=LABEL_CLR)
    plt.tight_layout(pad=0.8)
    st.pyplot(fig, use_container_width=True)
    plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

with r3c2:
    st.markdown('<div class="chart-wrap"><div class="chart-title">Sector Drill-Down</div>', unsafe_allow_html=True)
    sectors = sorted(df["Sector"].unique())
    sel     = st.selectbox("Select Sector", ["All Sectors"] + sectors, label_visibility="collapsed")
    filt    = df if sel == "All Sectors" else df[df["Sector"] == sel]
    stocks  = filt.groupby("Stock_Name")["Total_Value"].sum().sort_values(ascending=False).head(6)
    mx      = stocks.max() if len(stocks) else 1

    for stk, val in stocks.items():
        pct = int(val / mx * 100)
        st.markdown(f"""
        <div class="prog-row">
            <div class="prog-meta">
                <span class="prog-name">{stk}</span>
                <span class="prog-val">{fmt_inr(val)}</span>
            </div>
            <div class="prog-track">
                <div class="prog-fill" style="width:{pct}%"></div>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ROW 4 — Quarterly Summary Table
# ─────────────────────────────────────────────
st.markdown('<div class="chart-wrap"><div class="chart-title">Quarterly Trade Summary</div>', unsafe_allow_html=True)
qtr = df.groupby(["Quarter","Transaction_Type"])["Total_Value"].sum().unstack(fill_value=0)
qtr["Net P&L"] = qtr.get("Sell", 0) - qtr.get("Buy", 0)
qtr = qtr.rename(columns={"Buy":"Buy Value","Sell":"Sell Value"})
for col in qtr.columns:
    qtr[col] = qtr[col].apply(fmt_inr)
st.dataframe(qtr, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# RAW DATA TABLE
# ─────────────────────────────────────────────
with st.expander("View Raw Transaction Data"):
    disp = df[["Date","Stock_Name","Sector","City","Transaction_Type","Quantity","Price_Per_Stock","Total_Value"]].copy()
    disp["Date"]        = disp["Date"].dt.strftime("%d %b %Y")
    disp["Total_Value"] = disp["Total_Value"].apply(fmt_inr)
    disp.columns        = ["Date","Stock","Sector","City","Type","Qty","Price / Share","Total Value"]
    st.dataframe(disp, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="pbi-footer">
    StockPulse Analytics &nbsp;&middot;&nbsp; FY 2024 &nbsp;&middot;&nbsp; NSE Large Cap &nbsp;&middot;&nbsp; Data is indicative and for demonstration purposes only
</div>""", unsafe_allow_html=True)