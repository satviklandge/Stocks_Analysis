import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import rcParams
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="StockPulse | Trading Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# GLOBAL STYLES
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background-color: #020817 !important;
    color: #E2E8F0 !important;
}

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="collapsedControl"] { display: none; }
section[data-testid="stSidebar"] { display: none !important; }

/* Main block */
.block-container {
    padding: 2rem 3rem !important;
    max-width: 1400px !important;
    background-color: #020817 !important;
}

/* Header banner */
.dash-header {
    background: linear-gradient(90deg, #0F172A 0%, #0A0F1E 100%);
    border: 1px solid #1E293B;
    border-radius: 16px;
    padding: 20px 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 28px;
}
.dash-logo {
    display: flex;
    align-items: center;
    gap: 14px;
}
.logo-icon {
    width: 44px; height: 44px;
    background: linear-gradient(135deg, #6366F1, #10B981);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px;
}
.logo-title { font-size: 22px; font-weight: 800; color: #F1F5F9; letter-spacing: -0.02em; }
.logo-sub   { font-size: 11px; color: #475569; letter-spacing: 0.08em; font-weight: 600; text-transform: uppercase; }
.live-badge {
    background: #10B98120; color: #10B981;
    border: 1px solid #10B98133;
    border-radius: 20px; padding: 5px 16px;
    font-size: 12px; font-weight: 700; letter-spacing: 0.04em;
}

/* KPI cards */
.kpi-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 16px; margin-bottom: 28px; }
.kpi-card {
    border-radius: 16px;
    padding: 22px 24px;
    position: relative;
    overflow: hidden;
}
.kpi-label  { font-size: 11px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #64748B; margin-bottom: 6px; }
.kpi-value  { font-size: 26px; font-weight: 800; color: #F1F5F9; letter-spacing: -0.02em; }
.kpi-sub    { font-size: 12px; font-weight: 600; margin-top: 4px; }

/* Section titles */
.section-title {
    display: flex; align-items: center; gap: 12px;
    margin-bottom: 16px; margin-top: 4px;
}
.title-bar {
    width: 4px; height: 22px;
    background: linear-gradient(180deg, #6366F1, #10B981);
    border-radius: 2px;
}
.title-text { font-size: 15px; font-weight: 700; color: #E2E8F0; margin: 0; }

/* Chart cards */
.chart-card {
    background: #0F172A;
    border: 1px solid #1E293B;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
}

/* Sector pills */
.pill-row { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 16px; }
.pill {
    border-radius: 20px; padding: 5px 16px;
    font-size: 11px; font-weight: 700;
    letter-spacing: 0.04em; cursor: pointer;
    display: inline-block;
}

/* Progress bars */
.prog-label { display: flex; justify-content: space-between; margin-bottom: 4px; }
.prog-name  { font-size: 13px; font-weight: 600; color: #CBD5E1; }
.prog-val   { font-size: 12px; color: #94A3B8; }
.prog-track { background: #1E293B; border-radius: 4px; height: 7px; margin-bottom: 10px; }
.prog-fill  { height: 100%; border-radius: 4px; background: linear-gradient(90deg,#6366F1,#10B981); }

/* Table */
.stDataFrame { background: #0F172A !important; }
thead tr th { background: #0F172A !important; color: #64748B !important; font-size: 11px !important; font-weight: 700 !important; text-transform: uppercase !important; letter-spacing: 0.06em !important; border-bottom: 1px solid #1E293B !important; }
tbody tr td { color: #CBD5E1 !important; font-size: 13px !important; border-bottom: 1px solid #0F172A !important; }
tbody tr:hover td { background: #1E293B !important; }

/* Footer */
.dash-footer { text-align: center; color: #334155; font-size: 11px; font-weight: 500; letter-spacing: 0.06em; padding-top: 24px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MATPLOTLIB THEME
# ─────────────────────────────────────────────
BG     = "#0F172A"
BORDER = "#1E293B"
TEXT   = "#94A3B8"
WHITE  = "#E2E8F0"

plt.rcParams.update({
    "figure.facecolor":  BG,
    "axes.facecolor":    BG,
    "axes.edgecolor":    BORDER,
    "axes.labelcolor":   TEXT,
    "xtick.color":       TEXT,
    "ytick.color":       TEXT,
    "text.color":        WHITE,
    "grid.color":        BORDER,
    "font.family":       "sans-serif",
    "font.size":         11,
})

PALETTE = {
    "Energy":         "#F59E0B",
    "IT":             "#7B1162",  
    "Banking":        "#3FF45d",
    "Finance":        "#10B981",
    "Auto":           "#7B1162",
    "Pharma":         "#8B5CF6",
    "Infrastructure": "#0EA5E9",
    "FMCG":           "#EC4899",
}
PIE_COLORS = list(PALETTE.values())

# ─────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("stock_data_sale.csv")
        df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
    except FileNotFoundError:
        rows = [
            ("2024-01-05","Reliance","Energy","Mumbai","Buy",120,2450),
            ("2024-01-10","TCS","IT","Bangalore","Buy",80,3800),
            ("2024-01-15","HDFC Bank","Finance","Mumbai","Buy",200,1600),
            ("2024-02-03","Infosys","IT","Hyderabad","Buy",150,1480),
            ("2024-02-14","Reliance","Energy","Delhi","Sell",60,2600),
            ("2024-02-20","TCS","IT","Pune","Sell",40,4100),
            ("2024-03-01","ONGC","Energy","Chennai","Buy",300,210),
            ("2024-03-12","SBI","Finance","Kolkata","Buy",250,620),
            ("2024-03-22","Wipro","IT","Bangalore","Buy",180,480),
            ("2024-04-05","HDFC Bank","Finance","Mumbai","Sell",100,1750),
            ("2024-04-18","Infosys","IT","Hyderabad","Sell",80,1620),
            ("2024-04-28","Maruti","Auto","Delhi","Buy",50,9800),
            ("2024-05-07","SBI","Finance","Kolkata","Sell",120,680),
            ("2024-05-19","ONGC","Energy","Chennai","Sell",150,245),
            ("2024-05-30","Sun Pharma","Pharma","Mumbai","Buy",90,1200),
            ("2024-06-10","Maruti","Auto","Delhi","Sell",25,10500),
            ("2024-06-21","Wipro","IT","Bangalore","Sell",90,540),
            ("2024-07-03","ICICI Bank","Finance","Pune","Buy",160,1050),
            ("2024-07-15","Sun Pharma","Pharma","Mumbai","Sell",45,1380),
            ("2024-07-28","L&T","Infrastructure","Chennai","Buy",70,3600),
            ("2024-08-08","Reliance","Energy","Mumbai","Buy",80,2700),
            ("2024-08-20","ICICI Bank","Finance","Pune","Sell",80,1180),
            ("2024-09-05","L&T","Infrastructure","Delhi","Sell",35,3900),
            ("2024-09-17","TCS","IT","Bangalore","Buy",100,4300),
            ("2024-10-02","HUL","FMCG","Mumbai","Buy",120,2700),
            ("2024-10-14","TCS","IT","Hyderabad","Sell",60,4550),
            ("2024-11-06","HUL","FMCG","Chennai","Sell",60,2850),
            ("2024-11-18","Bajaj Auto","Auto","Pune","Buy",40,7200),
            ("2024-12-03","Bajaj Auto","Auto","Delhi","Sell",20,7800),
            ("2024-12-20","SBI","Finance","Kolkata","Buy",300,700),
        ]
        df = pd.DataFrame(rows, columns=["Date","Stock_Name","Sector","City","Transaction_Type","Quantity","Price_Per_Stock"])
        df["Date"] = pd.to_datetime(df["Date"])

    df["Total_Value"] = df["Quantity"] * df["Price_Per_Stock"]
    df["Month"]       = df["Date"].dt.month
    df["Month_Name"]  = df["Date"].dt.strftime("%b")
    return df

df = load_data()

def fmt_inr(n):
    if n >= 1e7:  return f"₹{n/1e7:.2f} Cr"
    if n >= 1e5:  return f"₹{n/1e5:.2f} L"
    return f"₹{n:,.0f}"

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="dash-header">
  <div class="dash-logo">
    <div class="logo-icon">📈</div>
    <div>
      <div class="logo-title">StockPulse</div>
      <div class="logo-sub">Trading Analytics Dashboard</div>
    </div>
  </div>
  <div class="live-badge">● LIVE DATA &nbsp;|&nbsp; FY 2024</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# KPI METRICS
# ─────────────────────────────────────────────
buy_val   = df[df.Transaction_Type == "Buy"]["Total_Value"].sum()
sell_val  = df[df.Transaction_Type == "Sell"]["Total_Value"].sum()
profit    = sell_val - buy_val
top_stock = df.groupby("Stock_Name")["Total_Value"].sum().idxmax()
pnl_pct   = (profit / buy_val * 100) if buy_val else 0
pnl_color = "#10B981" if profit >= 0 else "#F43F5E"
pnl_arrow = "▲" if profit >= 0 else "▼"

kpi_data = [
    ("💰", "Total Investment", fmt_inr(buy_val),  "Capital deployed",          "#6366F1"),
    ("💵", "Total Sell Value", fmt_inr(sell_val), "Revenue realized",           "#0EA5E9"),
    ("📊", "Net P&L",          fmt_inr(abs(profit)), f"{pnl_arrow} {abs(pnl_pct):.1f}% return", pnl_color),
    ("🏆", "Top Stock",        top_stock,          "By total value",             "#F59E0B"),
]

cols = st.columns(4)
for col, (icon, label, value, sub, color) in zip(cols, kpi_data):
    with col:
        st.markdown(f"""
        <div class="kpi-card" style="background:linear-gradient(135deg,#0F172A 60%,{color}18);border:1px solid {color}33;">
            <div style="font-size:28px;margin-bottom:8px">{icon}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-sub" style="color:{color}">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='margin-bottom:8px'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ROW 1 — Most Traded | Monthly Trend
# ─────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title"><div class="title-bar"></div><p class="title-text">Most Traded Stocks</p></div>', unsafe_allow_html=True)

    most_traded = df.groupby("Stock_Name")["Quantity"].sum().sort_values(ascending=False).head(8)

    bar_colors = plt.cm.tab10(np.linspace(0, 1, len(most_traded)))

    fig, ax = plt.subplots(figsize=(6, 3.4))
    bars = ax.bar(most_traded.index, most_traded.values, color=bar_colors, width=0.6, zorder=3)
    ax.set_facecolor(BG); fig.patch.set_facecolor(BG)
    ax.yaxis.grid(True, linestyle="--", alpha=0.4, color=BORDER, zorder=0)
    ax.set_axisbelow(True)
    ax.spines[:].set_visible(False)
    ax.tick_params(axis="x", rotation=30, labelsize=10)
    ax.tick_params(axis="y", labelsize=10)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x,_: f"{int(x/1000)}K" if x>=1000 else str(int(x))))
    for bar in bars:
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+5,
                str(int(bar.get_height())), ha="center", va="bottom", fontsize=9, color=TEXT)
    plt.tight_layout(pad=1)
    st.pyplot(fig, use_container_width=True)
    plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title"><div class="title-bar"></div><p class="title-text">Monthly Trading Trend</p></div>', unsafe_allow_html=True)

    monthly = df.groupby("Month")["Total_Value"].sum().reindex(range(1,13), fill_value=0)
    month_labels = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    fig, ax = plt.subplots(figsize=(6, 3.4))
    ax.fill_between(range(12), monthly.values, alpha=0.15, color="#6366F1")
    ax.plot(range(12), monthly.values, color="#6366F1", linewidth=2.5, marker="o",
            markersize=6, markerfacecolor="#818CF8", markeredgewidth=2, markeredgecolor="#6366F1", zorder=4)
    ax.set_xticks(range(12)); ax.set_xticklabels(month_labels, fontsize=10)
    ax.yaxis.grid(True, linestyle="--", alpha=0.4, color=BORDER, zorder=0)
    ax.set_axisbelow(True); ax.spines[:].set_visible(False); ax.set_facecolor(BG); fig.patch.set_facecolor(BG)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x,_: f"{x/1e5:.0f}L" if x>=1e5 else f"{x/1000:.0f}K"))
    plt.tight_layout(pad=1)
    st.pyplot(fig, use_container_width=True)
    plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ROW 2 — Sector Bar | Pie
# ─────────────────────────────────────────────
col3, col4 = st.columns([1.4, 1])

with col3:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title"><div class="title-bar"></div><p class="title-text">Sector-wise Investment</p></div>', unsafe_allow_html=True)

    sector_data = df.groupby("Sector")["Total_Value"].sum().sort_values(ascending=True)
    s_colors    = [PALETTE.get(s, "#6366F1") for s in sector_data.index]

    fig, ax = plt.subplots(figsize=(7, 3.6))
    bars = ax.barh(sector_data.index, sector_data.values, color=s_colors, height=0.55, zorder=3)
    ax.xaxis.grid(True, linestyle="--", alpha=0.4, color=BORDER, zorder=0)
    ax.set_axisbelow(True); ax.spines[:].set_visible(False); ax.set_facecolor(BG); fig.patch.set_facecolor(BG)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x,_: f"{x/1e5:.0f}L"))
    ax.tick_params(labelsize=10)
    for bar in bars:
        w = bar.get_width()
        ax.text(w + w*0.02, bar.get_y()+bar.get_height()/2,
                fmt_inr(w), va="center", fontsize=9, color=TEXT)
    plt.tight_layout(pad=1)
    st.pyplot(fig, use_container_width=True)
    plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title"><div class="title-bar"></div><p class="title-text">Sector Distribution</p></div>', unsafe_allow_html=True)

    sector_pie = df.groupby("Sector")["Total_Value"].sum()
    pie_colors = [PALETTE.get(s, "#6366F1") for s in sector_pie.index]

    fig, ax = plt.subplots(figsize=(4.5, 3.6))
    wedges, texts, autotexts = ax.pie(
        sector_pie.values,
        labels=None,
        autopct="%1.1f%%",
        colors=pie_colors,
        startangle=140,
        pctdistance=0.78,
        wedgeprops=dict(width=0.55, edgecolor=BG, linewidth=2),
    )
    for at in autotexts:
        at.set_fontsize(9); at.set_color(WHITE); at.set_fontweight("600")
    ax.set_facecolor(BG); fig.patch.set_facecolor(BG)
    patches = [mpatches.Patch(color=pie_colors[i], label=s) for i, s in enumerate(sector_pie.index)]
    ax.legend(handles=patches, loc="lower center", bbox_to_anchor=(0.5,-0.08),
              ncol=2, fontsize=9, frameon=False, labelcolor=TEXT)
    plt.tight_layout(pad=0.5)
    st.pyplot(fig, use_container_width=True)
    plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ROW 3 — City Chart | Sector Drill-down
# ─────────────────────────────────────────────
col5, col6 = st.columns(2)

with col5:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title"><div class="title-bar"></div><p class="title-text">City-wise Trading Activity</p></div>', unsafe_allow_html=True)

    city_data = df.groupby("City")["Total_Value"].sum().sort_values(ascending=False)
    city_colors = plt.cm.Set3(np.linspace(0, 1, len(city_data)))

    fig, ax = plt.subplots(figsize=(6, 3.4))
    bars = ax.bar(city_data.index, city_data.values, color=city_colors, width=0.55, zorder=3)
    ax.yaxis.grid(True, linestyle="--", alpha=0.4, color=BORDER, zorder=0)
    ax.set_axisbelow(True); ax.spines[:].set_visible(False); ax.set_facecolor(BG); fig.patch.set_facecolor(BG)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x,_: f"{x/1e5:.0f}L"))
    ax.tick_params(axis="x", rotation=20, labelsize=10); ax.tick_params(axis="y", labelsize=10)
    for bar in bars:
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+bar.get_height()*0.02,
                fmt_inr(bar.get_height()), ha="center", va="bottom", fontsize=9, color=TEXT)
    plt.tight_layout(pad=1)
    st.pyplot(fig, use_container_width=True)
    plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

with col6:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title"><div class="title-bar"></div><p class="title-text">Sector Drill-down</p></div>', unsafe_allow_html=True)

    sectors    = sorted(df["Sector"].unique())
    sel_sector = st.selectbox("Filter by Sector", ["All Sectors"] + sectors,
                               label_visibility="collapsed")

    filt_df    = df if sel_sector == "All Sectors" else df[df["Sector"] == sel_sector]
    top_stocks = filt_df.groupby("Stock_Name")["Total_Value"].sum().sort_values(ascending=False).head(6)
    max_val    = top_stocks.max() if len(top_stocks) else 1

    for stock, val in top_stocks.items():
        pct = int(val / max_val * 100)
        st.markdown(f"""
        <div>
          <div class="prog-label">
            <span class="prog-name">{stock}</span>
            <span class="prog-val">{fmt_inr(val)}</span>
          </div>
          <div class="prog-track">
            <div class="prog-fill" style="width:{pct}%"></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ROW 4 — Buy vs Sell by Month
# ─────────────────────────────────────────────
st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title"><div class="title-bar"></div><p class="title-text">Buy vs Sell — Monthly Comparison</p></div>', unsafe_allow_html=True)

buy_monthly  = df[df.Transaction_Type=="Buy"].groupby("Month")["Total_Value"].sum().reindex(range(1,13),fill_value=0)
sell_monthly = df[df.Transaction_Type=="Sell"].groupby("Month")["Total_Value"].sum().reindex(range(1,13),fill_value=0)
x = np.arange(12); w = 0.38
month_labels = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

fig, ax = plt.subplots(figsize=(13, 3.4))
ax.bar(x - w/2, buy_monthly.values,  w, color="#6366F1", label="Buy",  zorder=3, alpha=0.9)
ax.bar(x + w/2, sell_monthly.values, w, color="#10B981", label="Sell", zorder=3, alpha=0.9)
ax.set_xticks(x); ax.set_xticklabels(month_labels, fontsize=10)
ax.yaxis.grid(True, linestyle="--", alpha=0.4, color=BORDER, zorder=0)
ax.set_axisbelow(True); ax.spines[:].set_visible(False); ax.set_facecolor(BG); fig.patch.set_facecolor(BG)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x,_: f"{x/1e5:.0f}L" if x>=1e5 else f"{x/1000:.0f}K"))
ax.legend(fontsize=11, frameon=False, labelcolor=WHITE)
plt.tight_layout(pad=1)
st.pyplot(fig, use_container_width=True)
plt.close()
st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# RAW DATA TABLE (collapsible)
# ─────────────────────────────────────────────
with st.expander("🗂️  View Raw Transaction Data"):
    display_df = df[["Date","Stock_Name","Sector","City","Transaction_Type","Quantity","Price_Per_Stock","Total_Value"]].copy()
    display_df["Date"]        = display_df["Date"].dt.strftime("%d %b %Y")
    display_df["Total_Value"] = display_df["Total_Value"].apply(fmt_inr)
    display_df.columns        = ["Date","Stock","Sector","City","Type","Qty","Price/Share","Total Value"]
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown('<div class="dash-footer">STOCKPULSE ANALYTICS · FY2024 · POWERED BY STREAMLIT</div>', unsafe_allow_html=True)