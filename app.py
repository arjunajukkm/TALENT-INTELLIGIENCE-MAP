import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import textwrap
import base64

# =============================================================================
# 0) PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="FinBox Talent | 9-Box Grid",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# 1) FINBOX THEME & COLORS (FORCED DARK)
# =============================================================================
FINBOX = {
    "blue": "#194CFF",
    "green": "#10B981",
    "bg":   "#F7FAFF", 
    "card": "#FFFFFF", 
    "text": "#0F172A", 
    "muted":"#64748B",
    "line": "#E6EEF8"
}

NINE_BOX = {
    "Rough Diamond": "#ff8700",       
    "Future Leader": "#B6F500",       
    "Top Talent": "#2d00f7",          
    "Inconsistent Player": "#ffd60a", 
    "The Keystone": "#0aff99",        
    "Impact Driver": "#FF2DD1",       
    "Talent Mismatch": "#ff0000",     
    "Practitioner": "#be0aff",        
    "Trusted Advisor": "#FFFCFB",     
    "New to Rate": "#c8c7d6"
}

BOX_DEFINITIONS = {
    "Top Talent": "Top talent. Consistently exceeds expectations. Retain at all costs.",
    "Future Leader": "High potential, still learning to deliver top results.",
    "Rough Diamond": "High raw talent but failing to deliver. Miscast role?",
    "Impact Driver": "Excellent results, steady growth. Key asset.",
    "The Keystone": "Reliable backbone. Meets expectations consistently.",
    "Inconsistent Player": "Inconsistent results. Needs coaching to decide future.",
    "Trusted Advisor": "Deep technical expert. Great executor, limited leadership.",
    "Practitioner": "Meets basic requirements, limited scope for growth.",
    "Talent Mismatch": "Not meeting expectations. Requires exit plan.",
    "New to Rate": "Not enough data to evaluate."
}

# FORCED DARK MODE VARIABLES
def theme_vars():
    return {
        "--fb-bg": "#070A12",
        "--fb-card": "#0B1020",
        "--fb-text": "#E5E7EB",
        "--fb-muted": "#9CA3AF",
        "--fb-border": "rgba(148, 163, 184, 0.18)",
        "--fb-blue": FINBOX["blue"],
        "--fb-shadow": "0 18px 50px rgba(0,0,0,0.45)",
        "--fb-grid": "rgba(148,163,184,0.12)",
        "--fb-axis": "rgba(148,163,184,0.70)",
        "--fb-sidebar": "#0B1020",
        "--plotly-temp": "plotly_dark",
        "--fb-card2": "linear-gradient(180deg, rgba(11,16,32,0.95), rgba(11,16,32,0.88))",
        "--fb-scroll-thumb": "rgba(148, 163, 184, 0.3)",
        "--fb-scroll-track": "rgba(0,0,0,0.2)",
    }

vars_ = theme_vars()

def _img_to_data_uri(path: str):
    ext = os.path.splitext(path)[1].lower().replace(".", "")
    if ext == "jpg": ext = "jpeg"
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/{ext};base64,{b64}"

def get_wordmark_src():
    candidates = ["FinBox Logo with wordmark.svg", "FinBox Logo with wordmark.png", "FinBox Logo with wordmark.jpg"]
    for c in candidates:
        if os.path.exists(c): return _img_to_data_uri(c)
    return None

WORDMARK_SRC = get_wordmark_src()

st.markdown(
    textwrap.dedent(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800;900&display=swap');
    :root {{ {''.join([f"{k}:{v};" for k,v in vars_.items()])} }}
    html, body, [class*="css"], [data-testid="stAppViewContainer"] {{
      font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
      background: var(--fb-bg) !important;
      color: var(--fb-text) !important;
    }}
    [data-testid="stSidebar"] {{ background-color: var(--fb-sidebar) !important; border-right: 1px solid var(--fb-border); }}
    .block-container {{ padding-top: 1rem; padding-bottom: 2rem; padding-left: 1.5rem; padding-right: 1.5rem; max-width: 100% !important; }}
    
    /* TABS */
    .stTabs [data-baseweb="tab-list"] {{ gap: 24px; border-bottom: none !important; padding-bottom: 0px !important; margin-bottom: 0px !important; }}
    .stTabs [data-baseweb="tab-border"], .stTabs [data-baseweb="tab-highlight"] {{ display: none !important; visibility: hidden !important; }}
    .stTabs [data-baseweb="tab"] {{ height: 40px; white-space: pre-wrap; background-color: transparent; color: var(--fb-muted); font-weight: 600; border: none !important; padding-bottom: 0px; letter-spacing: -0.01em; font-size: 14px; }}
    .stTabs [data-baseweb="tab"][aria-selected="true"] {{ color: var(--fb-blue) !important; text-shadow: 0 0 0 rgba(0,0,0,0); font-weight: 700; border-bottom: 2px solid var(--fb-blue) !important; }}
    .stTabs [data-baseweb="tab-panel"] {{ padding-top: 10px !important; margin-top: 0px !important; }}

    /* HERO */
    .fb-hero {{
      border: 1px solid var(--fb-border);
      background: radial-gradient(900px 260px at 10% 0%, rgba(25,76,255,0.22), transparent 55%), radial-gradient(700px 260px at 88% 0%, rgba(34,211,238,0.14), transparent 52%), var(--fb-card2);
      box-shadow: var(--fb-shadow);
      border-radius: 16px;
      padding: 30px 34px;
      margin-bottom: 16px;
      display: flex; justify-content: space-between; align-items: center; gap: 18px; position: relative; overflow: hidden; width: 100%;
    }}
    .fb-hero:before {{ content: ""; position: absolute; inset: -2px; background: radial-gradient(900px 240px at 18% 0%, rgba(25,76,255,0.22), transparent 60%); opacity: 0.55; filter: blur(12px); pointer-events: none; }}
    
    /* HEADER STYLE */
    .fb-title {{ 
        position: relative; 
        font-weight: 900; 
        font-size: 30px !important; 
        text-transform: uppercase;
        letter-spacing: -0.03em; 
        margin: 0; 
        line-height: 1; 
        color: var(--fb-text); 
    }}
    
    .fb-logo {{ position: relative; display:flex; align-items:center; justify-content:flex-end; min-width: 340px; }}
    .fb-logo img {{ height: 54px; opacity: 0.95; filter: drop-shadow(0 10px 20px rgba(0,0,0,0.12)); }}

    /* KPI SCROLLABLE */
    .fb-kpis {{
        display: flex; flex-wrap: nowrap; gap: 12px; margin: 10px 0 22px 0;
        overflow-x: auto; padding-bottom: 8px; padding-left: 2px; padding-right: 2px;
        scroll-behavior: smooth; -webkit-overflow-scrolling: touch; scroll-snap-type: x mandatory;
    }}
    .fb-kpis::-webkit-scrollbar {{ height: 6px; background: transparent; }}
    .fb-kpis::-webkit-scrollbar-track {{ background: var(--fb-scroll-track); border-radius: 10px; }}
    .fb-kpis::-webkit-scrollbar-thumb {{ background-color: var(--fb-scroll-thumb); border-radius: 10px; border: 1px solid transparent; background-clip: content-box; }}
    .fb-kpis::-webkit-scrollbar-thumb:hover {{ background-color: var(--fb-blue); }}
    
    .fb-kpi {{
      border: 1px solid var(--fb-border); border-radius: 14px; padding: 14px;
      background: radial-gradient(600px 160px at 20% 0%, rgba(25,76,255,0.14), transparent 60%), var(--fb-card2);
      box-shadow: var(--fb-shadow); transition: transform 0.18s ease, border-color 0.18s ease;
      min-width: 145px; max-width: 145px; flex: 0 0 auto; scroll-snap-align: start;
      min-height: 90px; position: relative; overflow: hidden; display: flex; flex-direction: column; justify-content: center;
    }}
    .fb-kpi:hover {{ transform: translateY(-2px); border-color: rgba(25,76,255,0.42); box-shadow: var(--fb-shadow), var(--fb-glow); }}
    .fb-kpi-icon {{ position: absolute; top: 10px; right: 10px; font-size: 16px; opacity: 0.78; }}
    .fb-kpi-label {{ color: var(--fb-muted); font-size: 10px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px; }}
    .fb-kpi-value {{ font-size: 24px; font-weight: 900; color: var(--fb-text); letter-spacing: -0.02em; }}

    /* TABLE WRAP & FIXES */
    .fb-table-wrap {{ 
        border: 1px solid var(--fb-border); 
        border-radius: 16px; 
        background: var(--fb-card2); 
        box-shadow: var(--fb-shadow); 
        padding: 0px 0px 5px 0px; 
        margin-top: 10px; 
        overflow-x: auto; 
        width: 100%; 
    }}
    .fb-table-wrap::-webkit-scrollbar {{ height: 8px; background: transparent; }}
    .fb-table-wrap::-webkit-scrollbar-thumb {{ background-color: var(--fb-scroll-thumb); border-radius: 10px; }}

    [data-testid="stElementToolbar"] {{ display: none !important; }}
    div[data-testid="stDataFrame"] {{ background-color: transparent !important; border-radius: 14px; width: 100% !important; }}
    div[data-testid="stDataFrame"] > div {{ margin-top: 0px !important; }} 
    div[data-testid="stDataFrame"] thead tr th {{ position: sticky !important; top: 0 !important; z-index: 3 !important; background: var(--fb-card) !important; color: var(--fb-text) !important; border-bottom: 1px solid var(--fb-border) !important; padding-top: 12px !important; padding-bottom: 12px !important; }}
    body[data-theme="dark"] div[data-testid="stDataFrame"] thead tr th {{ background: #0B1020 !important; }}
    div[data-testid="stDataFrame"] tbody tr:hover td {{ background: rgba(25,76,255,0.06) !important; }}

    /* LOGIC CARD STYLES */
    .logic-card {{
        background: var(--fb-card); border: 1px solid var(--fb-border); border-radius: 12px;
        padding: 16px; margin-bottom: 12px; height: 100%; box-shadow: var(--fb-shadow);
        transition: 0.2s; display: flex; flex-direction: column;
    }}
    .logic-card:hover {{ border-color: var(--fb-blue); }}
    .logic-head {{ font-weight: 800; font-size: 14px; margin-bottom: 8px; display: flex; align-items: center; gap: 8px; }}
    .logic-desc {{ font-size: 13px; color: var(--fb-muted); line-height: 1.5; }}
    .logic-grid {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; margin-bottom: 20px; align-items: stretch; }}
    </style>
    """).strip(),
    unsafe_allow_html=True
)

# =============================================================================
# 2) DATA ENGINE
# =============================================================================
@st.cache_data(ttl=600, show_spinner=False)
def load_data():
    file_name = "Data.xlsx"
    if not os.path.exists(file_name):
        st.error(f"⚠️ File not found: **{file_name}**")
        st.info("Please ensure the Excel file is in the root directory.")
        return None

    try:
        df = pd.read_excel(file_name)
        
        perf_cols = ["OKR Last Quarter", "Quality of Output", "Ownership and Reliability", "Delivery"]
        pot_cols = ["Learning Ability", "Collaboration", "Feedback Reception", "Ownership Beyond Scope"]
        
        missing_cols = [c for c in perf_cols + pot_cols if c not in df.columns]
        if missing_cols:
            st.error("⚠️ **Missing Columns in Excel**")
            st.stop()

        for col in perf_cols + pot_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        # 1. Calc Weighted Scores
        df["X_Score"] = (
            (df["OKR Last Quarter"] * 0.30) +
            (df["Quality of Output"] * 0.30) +
            (df["Ownership and Reliability"] * 0.20) +
            (df["Delivery"] * 0.20)
        )
        df["Y_Score"] = (
            (df["Learning Ability"] * 0.20) +
            (df["Collaboration"] * 0.30) +
            (df["Feedback Reception"] * 0.30) +
            (df["Ownership Beyond Scope"] * 0.20)
        )

        # 2. Calc GLOBAL Ranks
        df["X_Pct"] = df["X_Score"].rank(pct=True)
        df["Y_Pct"] = df["Y_Score"].rank(pct=True)

        # 3. Helper to determine box based on Pct
        def get_box(x, y):
            # Boundaries
            is_x_low = x < 0.30
            is_x_high = x > 0.80 
            is_x_med = not (is_x_low or is_x_high)
            
            is_y_low = y < 0.30
            is_y_high = y > 0.80 
            is_y_med = not (is_y_low or is_y_high)

            if is_y_high:
                if is_x_high: return "Top Talent"
                if is_x_med:  return "Future Leader"
                if is_x_low:  return "Rough Diamond"
            if is_y_med:
                if is_x_high: return "Impact Driver"
                if is_x_med:  return "The Keystone"
                if is_x_low:  return "Inconsistent Player"
            if is_y_low:
                if is_x_high: return "Trusted Advisor"
                if is_x_med:  return "Practitioner"
                if is_x_low:  return "Talent Mismatch"
            return "The Keystone"

        # 4. Assign Global Rating
        df["Final Rating"] = df.apply(lambda r: "New to Rate" if str(r.get("Category","")).strip()=="New to Rate" else get_box(r["X_Pct"], r["Y_Pct"]), axis=1)
        df["Box_Def"] = df["Final Rating"].map(BOX_DEFINITIONS)

        # 5. Calc LOCAL (Team) Ranks & Ratings
        mask = df["Category"] != "New to Rate"
        
        df.loc[mask, "X_Pct_Team"] = df[mask].groupby("Manager")["X_Score"].rank(pct=True)
        df.loc[mask, "Y_Pct_Team"] = df[mask].groupby("Manager")["Y_Score"].rank(pct=True)
        
        df["Team_Rating"] = df.apply(
            lambda r: "New to Rate" if not mask[r.name] else get_box(r["X_Pct_Team"], r["Y_Pct_Team"]), 
            axis=1
        )
        
        # Determine Comparison Status
        def get_status(row):
            if row["Final Rating"] == "New to Rate": return "-"
            if row["Final Rating"] == row["Team_Rating"]: return "🟰"
            
            # Comparison: Org - Team
            avg_global = (row["X_Pct"] + row["Y_Pct"]) / 2
            avg_local = (row["X_Pct_Team"] + row["Y_Pct_Team"]) / 2
            
            if avg_global > avg_local + 0.03: return "⬆️ Higher in Org"
            if avg_global < avg_local - 0.03: return "⬇️ Lower in Org"
            return "🟰"

        df["Comparison"] = df.apply(get_status, axis=1)

        return df

    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
        return None

df = load_data()
if df is None: st.stop()

# =============================================================================
# 3) SIDEBAR (SPLIT LOGIC FOR TRENDS VS SNAPSHOTS)
# =============================================================================
with st.sidebar:
    st.markdown("### 🛠 Filters")
    
    # We maintain two DataFrames:
    # 1. trend_df: Contains ALL quarters (for the Trends tab)
    # 2. final_df: Contains only SELECTED quarters (for the other tabs)
    
    # --- Structural Filters (Applied to BOTH) ---
    trend_df = df.copy()
    struct_cols = ["Business Unit", "Department", "Sub Department", "Manager"]
    
    for col in struct_cols:
        if col in df.columns:
            options = sorted(trend_df[col].dropna().unique().tolist())
            selected = st.multiselect(col, options, placeholder=f"Select {col}")
            if selected:
                trend_df = trend_df[trend_df[col].isin(selected)]
    
    st.markdown("---")
    
    # --- Time Filter (Applied ONLY to final_df) ---
    final_df = trend_df.copy()
    if "Quarter" in df.columns:
        q_options = sorted(df["Quarter"].dropna().unique().tolist(), reverse=True)
        # Default to latest quarter if nothing selected, or handle multiselect
        sel_quarter = st.multiselect("Quarter (Affects non-trend tabs)", q_options, default=q_options[:1] if q_options else None)
        if sel_quarter:
            final_df = final_df[final_df["Quarter"].isin(sel_quarter)]

    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    
    csv_buffer = final_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", data=csv_buffer, file_name="talent_data.csv", mime="text/csv", use_container_width=True)

vars_ = theme_vars()
WORDMARK_SRC = get_wordmark_src()

# =============================================================================
# 4) HEADER & KPI
# =============================================================================
logo_html = f"""<img src="{WORDMARK_SRC}" alt="FinBox Wordmark" />""" if WORDMARK_SRC else """<div style="font-weight:900;color:var(--fb-text);font-size:14px;">FinBox</div>"""

# HEADER
st.markdown(
    textwrap.dedent(f"""
    <div class="fb-hero">
       <div><div class="fb-title">TALENT INTELLIGIENCE MAP</div></div>
       <div class="fb-logo">{logo_html}</div>
    </div>
    """).strip(), unsafe_allow_html=True
)

def kpi(label, value, color, icon):
    return textwrap.dedent(f"""
    <div class="fb-kpi">
      <div class="fb-kpi-icon">{icon}</div>
      <div style="height:4px; width:26px; background:{color}; border-radius:6px; margin-bottom:10px;"></div>
      <div class="fb-kpi-label">{label}</div>
      <div class="fb-kpi-value">{value}</div>
    </div>
    """).strip()

total_hc = len(final_df)
evaluated = len(final_df[final_df["Final Rating"] != "New to Rate"])

star_c = len(final_df[final_df["Final Rating"] == "Top Talent"])
rising_c = len(final_df[final_df["Final Rating"] == "Future Leader"])
enigma_c = len(final_df[final_df["Final Rating"] == "Rough Diamond"])
hi_perf_c = len(final_df[final_df["Final Rating"] == "Impact Driver"])
core_c = len(final_df[final_df["Final Rating"] == "The Keystone"])
dilemma_c = len(final_df[final_df["Final Rating"] == "Inconsistent Player"])
spec_c = len(final_df[final_df["Final Rating"] == "Trusted Advisor"])
effect_c = len(final_df[final_df["Final Rating"] == "Practitioner"])
under_c = len(final_df[final_df["Final Rating"] == "Talent Mismatch"])

kpi_html = textwrap.dedent(f"""
<div class="fb-kpis">
  {kpi("Total HC", total_hc, FINBOX["blue"], "👥")}
  {kpi("Evaluated", evaluated, FINBOX["green"], "📋")}
  {kpi("Top Talent", star_c, NINE_BOX["Top Talent"], "🌟")}
  {kpi("Future Leader", rising_c, NINE_BOX["Future Leader"], "🚀")}
  {kpi("Rough Diamond", enigma_c, NINE_BOX["Rough Diamond"], "💎")}
  {kpi("Impact Driver", hi_perf_c, NINE_BOX["Impact Driver"], "⚡")}
  {kpi("The Keystone", core_c, NINE_BOX["The Keystone"], "🧱")}
  {kpi("Inconsistent", dilemma_c, NINE_BOX["Inconsistent Player"], "⚠️")}
  {kpi("Trusted Advisor", spec_c, NINE_BOX["Trusted Advisor"], "🎓")}
  {kpi("Practitioner", effect_c, NINE_BOX["Practitioner"], "🛡️")}
  {kpi("Mismatch", under_c, NINE_BOX["Talent Mismatch"], "⛔")}
</div>
""").strip()
st.markdown(kpi_html, unsafe_allow_html=True)

# =============================================================================
# 6) CHART LOGIC
# =============================================================================
def build_quadrant_chart(filtered_data, global_data):
    try:
        x_30 = np.percentile(global_data["X_Score"], 30)
        x_80 = np.percentile(global_data["X_Score"], 80)
        y_30 = np.percentile(global_data["Y_Score"], 30)
        y_80 = np.percentile(global_data["Y_Score"], 80)
    except:
        x_30, x_80, y_30, y_80 = 3, 8, 3, 8

    fig = go.Figure()

    for rate, color in NINE_BOX.items():
        if rate == "New to Rate": continue
        d = filtered_data[filtered_data["Final Rating"] == rate]
        if d.empty: continue
        
        d_grouped = d.groupby(['X_Score', 'Y_Score']).agg(
            Emp_List=('EMP Name', lambda x: '• ' + '<br>• '.join(x)),
            Count=('EMP Name', 'count'),
            Managers=('Manager', lambda x: ', '.join(x.unique()) if x.nunique() <= 2 else "Multiple"),
            Depts=('Department', lambda x: ', '.join(x.unique()) if x.nunique() <= 2 else "Multiple")
        ).reset_index()

        sizes = 14 + (d_grouped['Count'] - 1) * 6 

        fig.add_trace(go.Scatter(
            x=d_grouped["X_Score"], y=d_grouped["Y_Score"], mode="markers",
            marker=dict(size=sizes, color=color, opacity=0.85, line=dict(width=1, color="white")),
            name=rate,
            customdata=d_grouped[['Emp_List', 'Managers', 'Depts', 'Count']],
            hovertemplate=(
                "<b>%{customdata[3]} Employee(s)</b><br><br>" +
                "%{customdata[0]}<br><br>" + 
                "<b>Perf:</b> %{x:.1f} | <b>Pot:</b> %{y:.1f}<br>" +
                "<span style='color:#bbb'>----------------</span><br>" +
                "<b>Dept:</b> %{customdata[2]}<br><b>Mgr:</b> %{customdata[1]}<extra></extra>"
            )
        ))

    line_style = dict(color=vars_["--fb-axis"], width=1, dash="dot")
    max_range = 10.5 
    fig.add_shape(type="line", x0=x_30, y0=0, x1=x_30, y1=max_range, line=line_style)
    fig.add_shape(type="line", x0=x_80, y0=0, x1=x_80, y1=max_range, line=line_style)
    fig.add_shape(type="line", x0=0, y0=y_30, x1=max_range, y1=y_30, line=line_style)
    fig.add_shape(type="line", x0=0, y0=y_80, x1=max_range, y1=y_80, line=line_style)

    x_low_mid, x_med_mid, x_hi_mid = x_30/2, (x_30+x_80)/2, (x_80+max_range)/2
    y_low_mid, y_med_mid, y_hi_mid = y_30/2, (y_30+y_80)/2, (y_80+max_range)/2
    label_font = dict(size=11, weight="bold")

    fig.add_annotation(x=x_low_mid, y=y_hi_mid, text="ROUGH DIAMOND", showarrow=False, font=dict(color=NINE_BOX["Rough Diamond"], **label_font))
    fig.add_annotation(x=x_med_mid, y=y_hi_mid, text="FUTURE LEADER", showarrow=False, font=dict(color=NINE_BOX["Future Leader"], **label_font))
    fig.add_annotation(x=x_hi_mid,  y=y_hi_mid, text="TOP TALENT", showarrow=False, font=dict(color=NINE_BOX["Top Talent"], **label_font))
    fig.add_annotation(x=x_low_mid, y=y_med_mid, text="INCONSISTENT", showarrow=False, font=dict(color=NINE_BOX["Inconsistent Player"], **label_font))
    fig.add_annotation(x=x_med_mid, y=y_med_mid, text="THE KEYSTONE", showarrow=False, font=dict(color=NINE_BOX["The Keystone"], **label_font))
    fig.add_annotation(x=x_hi_mid,  y=y_med_mid, text="IMPACT DRIVER", showarrow=False, font=dict(color=NINE_BOX["Impact Driver"], **label_font))
    fig.add_annotation(x=x_low_mid, y=y_low_mid, text="TALENT MISMATCH", showarrow=False, font=dict(color=NINE_BOX["Talent Mismatch"], **label_font))
    fig.add_annotation(x=x_med_mid, y=y_low_mid, text="PRACTITIONER", showarrow=False, font=dict(color=NINE_BOX["Practitioner"], **label_font))
    fig.add_annotation(x=x_hi_mid,  y=y_low_mid, text="TRUSTED ADVISOR", showarrow=False, font=dict(color=NINE_BOX["Trusted Advisor"], **label_font))

    fig.update_layout(
        template=vars_["--plotly-temp"], height=650, margin=dict(l=20, r=20, t=10, b=20),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(title="Performance (Weighted)", range=[0, 10.5], showgrid=False, zeroline=False),
        yaxis=dict(title="Potential (Weighted)", range=[0, 10.5], showgrid=False, zeroline=False),
        legend=dict(orientation="h", y=1.02, x=1, xanchor="right"),
        font=dict(family="Inter", color=vars_["--fb-text"]),
    )
    return fig

# =============================================================================
# 7) MAIN CONTENT (TABS)
# =============================================================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📌 Overview", "🧭 Quadrant", "⚖️ Org vs Team", "👥 People", "📈 Trends", "ℹ️ Logic Guide"])

TABLE_ROWS = 7
TABLE_HEIGHT = 36 * (TABLE_ROWS + 1) + 12

# --- TAB 1: OVERVIEW ---
with tab1:
    c1, c2 = st.columns([1, 1.3])
    with c1:
        st.markdown("#### Rating Distribution")
        dist = final_df["Final Rating"].value_counts().reset_index()
        dist.columns = ["Rating", "Count"]
        fig_pie = px.pie(dist, values="Count", names="Rating", hole=0.62, color="Rating", color_discrete_map=NINE_BOX)
        fig_pie.update_traces(textinfo='percent+label', textposition='outside')
        fig_pie.update_layout(
            template=vars_["--plotly-temp"], showlegend=False, height=260,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=10, b=10, l=10, r=10), font=dict(family="Inter", color=vars_["--fb-text"])
        )
        st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
    with c2:
        cols_to_show = ["EMP Name", "Department", "Manager"]
        valid_cols = [c for c in cols_to_show if c in final_df.columns]
        if valid_cols:
            t1, t2, t3 = st.tabs(["🌟 Top Talent", "⛔ Mismatch", "🧱 Keystone"])
            with t1:
                df_star = final_df[final_df["Final Rating"] == "Top Talent"][valid_cols]
                st.markdown('<div class="fb-table-wrap">', unsafe_allow_html=True)
                st.dataframe(df_star.head(TABLE_ROWS), use_container_width=True, hide_index=True, height=TABLE_HEIGHT)
                st.markdown('</div>', unsafe_allow_html=True)
            with t2:
                df_under = final_df[final_df["Final Rating"] == "Talent Mismatch"][valid_cols]
                st.markdown('<div class="fb-table-wrap">', unsafe_allow_html=True)
                st.dataframe(df_under.head(TABLE_ROWS), use_container_width=True, hide_index=True, height=TABLE_HEIGHT)
                st.markdown('</div>', unsafe_allow_html=True)
            with t3:
                df_core = final_df[final_df["Final Rating"] == "The Keystone"][valid_cols]
                st.markdown('<div class="fb-table-wrap">', unsafe_allow_html=True)
                st.dataframe(df_core.head(TABLE_ROWS), use_container_width=True, hide_index=True, height=TABLE_HEIGHT)
                st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 2: QUADRANT ---
with tab2:
    fig_quad = build_quadrant_chart(final_df, df)
    st.plotly_chart(fig_quad, use_container_width=True, config={'displayModeBar': False})

# --- TAB 3: ORG VS TEAM (UPDATED: Remove Filters, Add Quarter Col) ---
with tab3:
    st.markdown("#### ⚖️ Calibration Matrix")
    
    comp_df = final_df[final_df["Final Rating"] != "New to Rate"].copy()
    
    if not comp_df.empty:
        # Columns config: Added Quarter at the start
        display_comp_cols = ["Quarter", "EMP Name", "Business Unit", "Department", "Manager", "Team_Rating", "Final Rating", "Comparison"]
        display_comp_cols = [c for c in display_comp_cols if c in comp_df.columns]

        def color_arrow(val):
            if "⬆️" in str(val): return "color: #10B981; font-weight: bold;"
            if "⬇️" in str(val): return "color: #EF4444; font-weight: bold;"
            return "color: #94A3B8;"

        styled_df = comp_df[display_comp_cols].style.map(color_arrow, subset=["Comparison"])

        st.markdown('<div class="fb-table-wrap">', unsafe_allow_html=True)
        st.dataframe(
            styled_df,
            use_container_width=True, hide_index=True, height=600,
            column_config={
                "Quarter": st.column_config.TextColumn("Quarter", width="small"),
                "EMP Name": st.column_config.TextColumn("Employee", width="medium"),
                "Business Unit": st.column_config.TextColumn("Business Unit", width="medium"),
                "Department": st.column_config.TextColumn("Department", width="medium"),
                "Team_Rating": st.column_config.TextColumn("Team Rating", width="medium"),
                "Final Rating": st.column_config.TextColumn("Org Rating", width="medium"),
                "Comparison": st.column_config.TextColumn("Team to Org Change", width="small"),
            }
        )
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No data available for comparison.")

# --- TAB 4: PEOPLE (UPDATED: Remove Filters, Add Quarter Col) ---
with tab4:
    st.markdown("#### 🔍 Employee Search")
    
    view_df = final_df.copy()
    
    # 1. Search Bar (Full Width)
    search_term = st.text_input("Search Employee Name", placeholder="Type name to filter list...", label_visibility="collapsed")
    if search_term: 
        view_df = view_df[view_df["EMP Name"].str.contains(search_term, case=False, na=False)]

    # 2. Table with Quarter as first column
    base_cols = ["Quarter", "EMP ID", "EMP Name", "Business Unit", "Department", "Manager", "X_Score", "Y_Score", "Final Rating"]
    final_view_cols = [c for c in base_cols if c in view_df.columns]
    
    st.markdown('<div class="fb-table-wrap">', unsafe_allow_html=True)
    st.dataframe(
        view_df[final_view_cols], use_container_width=True, hide_index=True, height=600,
        column_config={
            "Quarter": st.column_config.TextColumn("Quarter", width="small"),
            "X_Score": st.column_config.ProgressColumn("Performance", min_value=0, max_value=10, format="%.1f"),
            "Y_Score": st.column_config.ProgressColumn("Potential", min_value=0, max_value=10, format="%.1f"),
            "Final Rating": st.column_config.TextColumn("Box Name", width="small")
        }
    )
    st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 5: TRENDS (NEW TAB) ---
with tab5:
    if "Quarter" not in trend_df.columns:
        st.error("⚠️ 'Quarter' column missing in data. Trends cannot be generated.")
    else:
        # Removed "Talent Trends" header
        
        # 1. HC Trend and Category Trend
        row_trends = st.columns([1, 1])
        
        # --- A) HC TREND ---
        with row_trends[0]:
            st.markdown("**Headcount Evolution**")
            hc_trend = trend_df.groupby("Quarter")["EMP ID"].nunique().reset_index()
            hc_trend.columns = ["Quarter", "Headcount"]
            
            fig_hc = px.area(hc_trend, x="Quarter", y="Headcount", markers=True)
            fig_hc.update_traces(line_color=FINBOX["blue"], fillcolor="rgba(25, 76, 255, 0.1)")
            fig_hc.update_layout(
                template=vars_["--plotly-temp"], height=300,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=10, b=10, l=0, r=0), font=dict(family="Inter", color=vars_["--fb-text"]),
                xaxis=dict(showgrid=False), yaxis=dict(showgrid=False)
            )
            st.plotly_chart(fig_hc, use_container_width=True, config={'displayModeBar': False})

        # --- B) CATEGORY TREND (Line Chart) ---
        with row_trends[1]:
            st.markdown("**Category Distribution Trend**")
            cat_trend = trend_df[trend_df["Final Rating"] != "New to Rate"].groupby(["Quarter", "Final Rating"]).size().reset_index(name="Count")
            
            # Create Line chart for categories
            fig_cat = px.line(
                cat_trend, x="Quarter", y="Count", color="Final Rating",
                color_discrete_map=NINE_BOX, markers=True
            )
            
            fig_cat.update_layout(
                template=vars_["--plotly-temp"], height=300, 
                showlegend=False, # REMOVED LEGEND
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=10, b=10, l=0, r=0), font=dict(family="Inter", color=vars_["--fb-text"]),
                xaxis=dict(showgrid=False), yaxis=dict(showgrid=False)
            )
            st.plotly_chart(fig_cat, use_container_width=True, config={'displayModeBar': False})

        st.markdown("---")

        # --- C) SINGLE EMPLOYEE TRAJECTORY VISUALIZER (Filtered) ---
        st.markdown("**🔍 Individual Performance Trajectory**")
        st.caption("Showing trajectory for all employees currently selected in the sidebar filters.")
        
        # Prepare Data for Trajectory (Y axis must be categorical sorted)
        rating_order = [
            "Talent Mismatch", "New to Rate", "Practitioner", "Inconsistent Player", 
            "Rough Diamond", "The Keystone", "Trusted Advisor", 
            "Future Leader", "Impact Driver", "Top Talent"
        ]
        
        # We use trend_df which is already filtered by sidebar (BU, Dept, Mgr)
        traj_df = trend_df[trend_df["EMP Name"].notna()].sort_values("Quarter")
        
        if not traj_df.empty:
            unique_emps = sorted(traj_df["EMP Name"].unique())
            
            # START EMPTY, but logic will fallback to ALL if empty
            sel_emps = st.multiselect("Filter Employees (Start typing...)", unique_emps, default=[])
            
            # Logic: If nothing selected in dropdown, show ALL filtered data. If selected, show subset.
            if sel_emps:
                final_traj_data = traj_df[traj_df["EMP Name"].isin(sel_emps)]
            else:
                final_traj_data = traj_df

            fig_traj = px.line(
                final_traj_data, 
                x="Quarter", 
                y="Final Rating", 
                color="EMP Name",
                markers=True
            )
            
            fig_traj.update_yaxes(categoryorder='array', categoryarray=rating_order)
            
            fig_traj.update_layout(
                template=vars_["--plotly-temp"], height=450,
                xaxis=dict(title="Quarter", showgrid=False),
                yaxis=dict(title="Category", showgrid=False),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", color=vars_["--fb-text"]),
                showlegend=False # REMOVED LEGEND
            )
            st.plotly_chart(fig_traj, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("No data available for trajectory analysis.")


# --- TAB 6: LOGIC GUIDE ---
with tab6:
    def logic_card(title, desc, color):
        return f"""
        <div class="logic-card" style="border-left: 4px solid {color};">
            <div class="logic-head" style="color:{color};">{title}</div>
            <div class="logic-desc">{desc}</div>
        </div>
        """
    
    st.markdown("### 📘 The 9-Box Grid Logic")
    st.markdown("<div class='logic-grid'>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1: 
        st.markdown(logic_card("💎 Rough Diamond (Low Perf / High Pot)", "High raw talent but failing to deliver. Miscast role or disengaged?", NINE_BOX["Rough Diamond"]), unsafe_allow_html=True)
    with c2: 
        st.markdown(logic_card("🚀 Future Leader (Med Perf / High Pot)", "High potential, still learning the ropes to deliver top results.", NINE_BOX["Future Leader"]), unsafe_allow_html=True)
    with c3: 
        st.markdown(logic_card("🌟 Top Talent (High Perf / High Pot)", "Top talent. Role model. Exceeds all expectations. Retain at all costs.", NINE_BOX["Top Talent"]), unsafe_allow_html=True)
    
    c4, c5, c6 = st.columns(3)
    with c4: 
        st.markdown(logic_card("⚠️ Inconsistent Player (Low Perf / Med Pot)", "Inconsistent results. Needs coaching to decide if they stay or go.", NINE_BOX["Inconsistent Player"]), unsafe_allow_html=True)
    with c5: 
        st.markdown(logic_card("🧱 The Keystone (Med Perf / Med Pot)", "Reliable backbone of the organization. Meets expectations consistently.", NINE_BOX["The Keystone"]), unsafe_allow_html=True)
    with c6: 
        st.markdown(logic_card("⚡ Impact Driver (High Perf / Med Pot)", "Excellent results, steady growth. Key asset to the team.", NINE_BOX["Impact Driver"]), unsafe_allow_html=True)
    
    c7, c8, c9 = st.columns(3)
    with c7: 
        st.markdown(logic_card("⛔ Talent Mismatch (Low / Low)", "Not meeting expectations in results or growth. Requires exit plan.", NINE_BOX["Talent Mismatch"]), unsafe_allow_html=True)
    with c8: 
        st.markdown(logic_card("🛡️ Practitioner (Med Perf / Low Pot)", "Meets basic requirements but has limited scope for future growth.", NINE_BOX["Practitioner"]), unsafe_allow_html=True)
    with c9: 
        st.markdown(logic_card("🎓 Trusted Advisor (High Perf / Low Pot)", "Deep technical expert. Great executor, limited leadership desire.", NINE_BOX["Trusted Advisor"]), unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown(f"""
    <div class="logic-grid">
        <div class="logic-card">
            <div class="logic-head">📊 Performance Weights (X)</div>
            <div style="display:flex; justify-content:space-between; margin-bottom:6px;"><span style="color:var(--fb-muted)">OKR Achievement</span> <b>30%</b></div>
            <div style="display:flex; justify-content:space-between; margin-bottom:6px;"><span style="color:var(--fb-muted)">Quality of Output</span> <b>30%</b></div>
            <div style="display:flex; justify-content:space-between; margin-bottom:6px;"><span style="color:var(--fb-muted)">Ownership</span> <b>20%</b></div>
            <div style="display:flex; justify-content:space-between; margin-bottom:6px;"><span style="color:var(--fb-muted)">Delivery Speed</span> <b>20%</b></div>
        </div>
        <div class="logic-card">
            <div class="logic-head">🌱 Potential Weights (Y)</div>
            <div style="display:flex; justify-content:space-between; margin-bottom:6px;"><span style="color:var(--fb-muted)">Collaboration</span> <b>30%</b></div>
            <div style="display:flex; justify-content:space-between; margin-bottom:6px;"><span style="color:var(--fb-muted)">Feedback Rcpt</span> <b>30%</b></div>
            <div style="display:flex; justify-content:space-between; margin-bottom:6px;"><span style="color:var(--fb-muted)">Learning Ability</span> <b>20%</b></div>
            <div style="display:flex; justify-content:space-between; margin-bottom:6px;"><span style="color:var(--fb-muted)">Beyond Scope</span> <b>20%</b></div>
        </div>
        <div class="logic-card">
            <div class="logic-head">📐 Percentile Distribution</div>
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:12px;">
                <div style="background:{NINE_BOX['Top Talent']}; width:12px; height:12px; border-radius:3px;"></div>
                <div><b>High (Top 20%)</b> <span style="color:var(--fb-muted); font-size:12px; display:block;">Score > 80th Percentile</span></div>
            </div>
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:12px;">
                <div style="background:{NINE_BOX['The Keystone']}; width:12px; height:12px; border-radius:3px;"></div>
                <div><b>Medium (Middle 50%)</b> <span style="color:var(--fb-muted); font-size:12px; display:block;">Score 30th - 80th Percentile</span></div>
            </div>
            <div style="display:flex; align-items:center; gap:10px;">
                <div style="background:{NINE_BOX['Talent Mismatch']}; width:12px; height:12px; border-radius:3px;"></div>
                <div><b>Low (Bottom 30%)</b> <span style="color:var(--fb-muted); font-size:12px; display:block;">Score < 30th Percentile</span></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)