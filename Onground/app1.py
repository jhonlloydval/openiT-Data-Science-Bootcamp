"""
Philippine Labor Market Analytics Dashboard
Capstone Project — Data Analytics Track
Stakeholder: Department of Labor and Employment (DOLE)
Data Source: PSA Labor Force Survey (LFS), 2019–2024
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PH Labor Market Analytics | DOLE Capstone",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;600;700&family=IBM+Plex+Mono&display=swap');

    html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }

    .main { background-color: #0d1117; }
    .block-container { padding: 1.5rem 2rem; }

    .kpi-card {
        background: linear-gradient(135deg, #161b22 0%, #1c2333 100%);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 0.5rem;
    }
    .kpi-label { color: #8b949e; font-size: 0.75rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; }
    .kpi-value { color: #e6edf3; font-size: 2rem; font-weight: 700; line-height: 1.1; }
    .kpi-delta-pos { color: #3fb950; font-size: 0.85rem; }
    .kpi-delta-neg { color: #f85149; font-size: 0.85rem; }

    .insight-card {
        background: #161b22;
        border-left: 4px solid #388bfd;
        border-radius: 0 8px 8px 0;
        padding: 1rem 1.2rem;
        margin-bottom: 1rem;
    }
    .insight-tag { color: #388bfd; font-size: 0.7rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; }
    .insight-title { color: #e6edf3; font-size: 1rem; font-weight: 600; margin: 0.2rem 0; }
    .insight-body { color: #8b949e; font-size: 0.88rem; line-height: 1.6; }
    .insight-action { color: #3fb950; font-size: 0.82rem; margin-top: 0.5rem; }

    .rec-card {
        background: #161b22;
        border: 1px solid #388bfd33;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
    }
    .rec-number { color: #388bfd; font-size: 1.4rem; font-weight: 700; }
    .rec-title { color: #e6edf3; font-size: 0.95rem; font-weight: 600; }
    .rec-body { color: #8b949e; font-size: 0.85rem; line-height: 1.5; margin-top: 0.3rem; }

    .limit-card {
        background: #1c1a00;
        border: 1px solid #9e6a0333;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.5rem;
        color: #d29922;
        font-size: 0.85rem;
    }

    .section-header {
        color: #e6edf3;
        font-size: 1.1rem;
        font-weight: 700;
        letter-spacing: 0.03em;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #21262d;
        margin-bottom: 1rem;
    }

    .stTabs [data-baseweb="tab-list"] { gap: 0.5rem; border-bottom: 1px solid #21262d; }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #8b949e;
        border: 1px solid transparent;
        border-radius: 6px 6px 0 0;
        padding: 0.4rem 1rem;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background: #161b22 !important;
        color: #e6edf3 !important;
        border-color: #30363d !important;
        border-bottom-color: #0d1117 !important;
    }

    .sidebar-label { color: #8b949e; font-size: 0.75rem; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 0.2rem; }
    h1 { color: #e6edf3 !important; font-weight: 700 !important; }
    h2, h3 { color: #c9d1d9 !important; }
</style>
""", unsafe_allow_html=True)

# ─── LOAD & CLEAN DATA ───────────────────────────────────────────────────────
@st.cache_data
def load_and_clean_data():
    """
    CLEANING STEPS APPLIED:
    1. Load raw CSV
    2. Strip whitespace from string columns
    3. Remove duplicate rows (none found, but checked)
    4. Handle missing values in Notes column (fill with empty string)
    5. Verify numeric ranges (rates must be 0–100, persons > 0)
    6. Add derived columns: Year-Quarter label, Island Group, COVID flag
    7. Cap any rate outliers beyond plausible range
    """
    df = pd.read_csv("ph_labor_raw_uncleaned.csv")

    # Step 1: Strip whitespace
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()

    # Step 2: Remove duplicates
    before = len(df)
    df = df.drop_duplicates()
    duplicates_removed = before - len(df)

    # Step 3: Fill nulls in Notes
    df["Notes"] = df["Notes"].fillna("")

    # Step 4: Validate numeric ranges
    rate_cols = ["Employment_Rate", "Unemployment_Rate", "Underemployment_Rate", "LFPR"]
    for col in rate_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[col] = df[col].clip(0, 100)

    df["Employed_Persons_000"] = pd.to_numeric(df["Employed_Persons_000"], errors="coerce")
    df["Unemployed_Persons_000"] = pd.to_numeric(df["Unemployed_Persons_000"], errors="coerce")

    # Step 5: Derived columns
    df["YQ"] = df["Year"].astype(str) + " " + df["Quarter"]
    df["Year"] = df["Year"].astype(int)

    island_map = {
        "NCR": "Luzon", "CAR": "Luzon", "Region I": "Luzon", "Region II": "Luzon",
        "Region III": "Luzon", "CALABARZON": "Luzon", "MIMAROPA": "Luzon",
        "Region V": "Luzon", "Region VI": "Visayas", "Region VII": "Visayas",
        "Region VIII": "Visayas", "Region IX": "Mindanao", "Region X": "Mindanao",
        "Region XI": "Mindanao", "Region XII": "Mindanao", "CARAGA": "Mindanao",
        "BARMM": "Mindanao"
    }
    df["Island_Group"] = df["Region"].map(island_map)
    df["COVID_Period"] = df.apply(
        lambda r: "COVID Peak" if (r["Year"] == 2020 and r["Quarter"] == "Q2")
        else ("COVID Recovery" if (r["Year"] == 2020 and r["Quarter"] in ["Q3","Q4"]) or r["Year"] == 2021
        else ("Pre-COVID" if r["Year"] < 2020 else "Post-COVID")), axis=1
    )

    cleaning_log = {
        "rows_loaded": before,
        "duplicates_removed": duplicates_removed,
        "nulls_filled": df["Notes"].eq("").sum(),
        "rows_final": len(df),
        "columns_added": ["YQ", "Island_Group", "COVID_Period"]
    }
    return df, cleaning_log

df, cleaning_log = load_and_clean_data()

# ─── PLOTLY THEME ────────────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#161b22",
    font=dict(family="IBM Plex Sans", color="#8b949e", size=12),
    title_font=dict(color="#e6edf3", size=14, family="IBM Plex Sans"),
    xaxis=dict(gridcolor="#21262d", linecolor="#30363d", tickcolor="#8b949e"),
    yaxis=dict(gridcolor="#21262d", linecolor="#30363d", tickcolor="#8b949e"),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#c9d1d9")),
    margin=dict(l=40, r=20, t=50, b=40)
)
COLORS = ["#388bfd", "#3fb950", "#f85149", "#d29922", "#a5d6ff", "#7ee787", "#ff7b72"]

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🇵🇭 PH Labor Analytics")
    st.markdown("<div class='sidebar-label'>Filter by Year</div>", unsafe_allow_html=True)
    years = sorted(df["Year"].unique())
    selected_years = st.multiselect("Year", years, default=years, label_visibility="collapsed")

    st.markdown("<div class='sidebar-label'>Filter by Island Group</div>", unsafe_allow_html=True)
    islands = df["Island_Group"].dropna().unique().tolist()
    selected_islands = st.multiselect("Island Group", islands, default=islands, label_visibility="collapsed")

    st.markdown("<div class='sidebar-label'>Filter by Region</div>", unsafe_allow_html=True)
    available_regions = df[df["Island_Group"].isin(selected_islands)]["Region"].unique().tolist()
    selected_regions = st.multiselect("Region", sorted(available_regions), default=sorted(available_regions), label_visibility="collapsed")

    st.markdown("---")
    st.markdown("<div class='sidebar-label'>Data Source</div>", unsafe_allow_html=True)
    st.markdown("<small style='color:#8b949e'>PSA Labor Force Survey (LFS)<br>2019–2024 | 17 Regions<br>[openstat.psa.gov.ph](https://openstat.psa.gov.ph)</small>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-label' style='margin-top:1rem'>Stakeholder</div>", unsafe_allow_html=True)
    st.markdown("<small style='color:#8b949e'>Department of Labor and Employment (DOLE)</small>", unsafe_allow_html=True)

# Filter data
fdf = df[
    df["Year"].isin(selected_years) &
    df["Island_Group"].isin(selected_islands) &
    df["Region"].isin(selected_regions)
]

# ─── HEADER ──────────────────────────────────────────────────────────────────
st.markdown("# Philippine Labor Market Analytics Dashboard")
st.markdown("<p style='color:#8b949e;margin-top:-0.5rem'>Capstone Project · Data Analytics Track · Stakeholder: DOLE · PSA LFS 2019–2024</p>", unsafe_allow_html=True)
st.markdown("---")

# ─── KPI CARDS ───────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

latest = df[df["Year"] == df["Year"].max()]
prev = df[df["Year"] == df["Year"].max() - 1]

avg_unemp_now = latest["Unemployment_Rate"].mean()
avg_unemp_prev = prev["Unemployment_Rate"].mean()
avg_unemp_delta = avg_unemp_now - avg_unemp_prev

avg_unemp_peak = df[df["Year"] == 2020]["Unemployment_Rate"].mean()

avg_underemp = latest["Underemployment_Rate"].mean()
ncr_unemp = latest[latest["Region"] == "NCR"]["Unemployment_Rate"].mean()
barmm_unemp = latest[latest["Region"] == "BARMM"]["Unemployment_Rate"].mean()

with col1:
    delta_cls = "kpi-delta-pos" if avg_unemp_delta < 0 else "kpi-delta-neg"
    delta_sym = "▼" if avg_unemp_delta < 0 else "▲"
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-label'>Avg Unemployment Rate (2024)</div>
        <div class='kpi-value'>{avg_unemp_now:.1f}%</div>
        <div class='{delta_cls}'>{delta_sym} {abs(avg_unemp_delta):.1f}pp vs 2023</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-label'>COVID-19 Peak (Q2 2020)</div>
        <div class='kpi-value'>{avg_unemp_peak:.1f}%</div>
        <div class='kpi-delta-neg'>▲ Worst quarter on record</div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-label'>Avg Underemployment (2024)</div>
        <div class='kpi-value'>{avg_underemp:.1f}%</div>
        <div class='kpi-delta-neg'>Still high despite recovery</div>
    </div>""", unsafe_allow_html=True)

with col4:
    gap = ncr_unemp - barmm_unemp
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-label'>NCR vs BARMM Gap (2024)</div>
        <div class='kpi-value'>{gap:.1f}pp</div>
        <div class='kpi-delta-neg'>NCR {ncr_unemp:.1f}% · BARMM {barmm_unemp:.1f}%</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── TABS ────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Trends", "🗺️ Regional Map", "🏝️ Island Groups", "🔍 Insights", "💡 Recommendations", "⚠️ Limitations"
])

# ════════════════════════════════════════════════════════
# TAB 1 — TRENDS
# ════════════════════════════════════════════════════════
with tab1:
    st.markdown("<div class='section-header'>National Unemployment & Underemployment Trends (2019–2024)</div>", unsafe_allow_html=True)

    nat = df.groupby(["Year", "Quarter"])[["Unemployment_Rate", "Underemployment_Rate", "LFPR", "Employment_Rate"]].mean().reset_index()
    nat["YQ"] = nat["Year"].astype(str) + " " + nat["Quarter"]
    nat = nat.sort_values(["Year", "Quarter"])

    # Chart 1: Dual line — unemployment + underemployment
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=nat["YQ"], y=nat["Unemployment_Rate"],
        name="Unemployment Rate", mode="lines+markers",
        line=dict(color="#f85149", width=2.5),
        marker=dict(size=6, color="#f85149"),
        hovertemplate="<b>%{x}</b><br>Unemployment: %{y:.1f}%<extra></extra>"
    ))
    fig1.add_trace(go.Scatter(
        x=nat["YQ"], y=nat["Underemployment_Rate"],
        name="Underemployment Rate", mode="lines+markers",
        line=dict(color="#d29922", width=2.5, dash="dash"),
        marker=dict(size=6, color="#d29922"),
        hovertemplate="<b>%{x}</b><br>Underemployment: %{y:.1f}%<extra></extra>"
    ))
    # COVID annotation
    fig1.add_vrect(
        x0="2020 Q2", x1="2020 Q3",
        fillcolor="#f85149", opacity=0.08,
        annotation_text="COVID Peak", annotation_position="top left",
        annotation_font=dict(color="#f85149", size=11)
    )
    fig1.update_layout(**PLOTLY_LAYOUT, title="National Unemployment vs Underemployment Rate (%)", height=380)
    st.plotly_chart(fig1, use_container_width=True)

    # Chart 2: LFPR + Employment Rate
    col_a, col_b = st.columns(2)
    with col_a:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=nat["YQ"], y=nat["LFPR"],
            name="LFPR", mode="lines+markers",
            line=dict(color="#388bfd", width=2.5),
            fill="tozeroy", fillcolor="rgba(56,139,253,0.08)"
        ))
        fig2.update_layout(**PLOTLY_LAYOUT, title="Labor Force Participation Rate (%)", height=300)
        st.plotly_chart(fig2, use_container_width=True)

    with col_b:
        # Year-over-year unemployment change bar
        yr_avg = df.groupby("Year")["Unemployment_Rate"].mean().reset_index()
        yr_avg["YoY"] = yr_avg["Unemployment_Rate"].diff()
        yr_avg_clean = yr_avg.dropna()
        colors_bar = ["#f85149" if v > 0 else "#3fb950" for v in yr_avg_clean["YoY"]]
        fig3 = go.Figure(go.Bar(
            x=yr_avg_clean["Year"].astype(str),
            y=yr_avg_clean["YoY"],
            marker_color=colors_bar,
            hovertemplate="<b>%{x}</b><br>YoY Change: %{y:+.2f}pp<extra></extra>"
        ))
        fig3.update_layout(**PLOTLY_LAYOUT, title="Year-over-Year Change in Unemployment (pp)", height=300)
        st.plotly_chart(fig3, use_container_width=True)

# ════════════════════════════════════════════════════════
# TAB 2 — REGIONAL
# ════════════════════════════════════════════════════════
with tab2:
    st.markdown("<div class='section-header'>Regional Unemployment Rate Comparison</div>", unsafe_allow_html=True)

    sel_year_reg = st.selectbox("Select Year", sorted(df["Year"].unique(), reverse=True), key="reg_year")
    reg_df = df[df["Year"] == sel_year_reg].groupby("Region")[["Unemployment_Rate", "Underemployment_Rate", "LFPR", "Employed_Persons_000"]].mean().reset_index()
    reg_df = reg_df.sort_values("Unemployment_Rate", ascending=True)

    # Horizontal bar — unemployment by region
    fig4 = go.Figure(go.Bar(
        x=reg_df["Unemployment_Rate"],
        y=reg_df["Region"],
        orientation="h",
        marker=dict(
            color=reg_df["Unemployment_Rate"],
            colorscale=[[0, "#3fb950"], [0.5, "#d29922"], [1, "#f85149"]],
            showscale=True,
            colorbar=dict(title=dict(text="Unemp %", font=dict(color="#8b949e")), tickfont=dict(color="#8b949e"))
        ),
        hovertemplate="<b>%{y}</b><br>Unemployment: %{x:.1f}%<extra></extra>"
    ))
    fig4.update_layout(**PLOTLY_LAYOUT, title=f"Unemployment Rate by Region ({sel_year_reg})", height=520, xaxis_title="Unemployment Rate (%)")
    st.plotly_chart(fig4, use_container_width=True)

    # Scatter: Unemployment vs Underemployment per region
    fig5 = px.scatter(
        reg_df, x="Unemployment_Rate", y="Underemployment_Rate",
        text="Region", size="Employed_Persons_000",
        color="Unemployment_Rate",
        color_continuous_scale=[[0, "#3fb950"], [0.5, "#d29922"], [1, "#f85149"]],
        hover_data={"Unemployment_Rate": ":.1f", "Underemployment_Rate": ":.1f"},
        title=f"Unemployment vs. Underemployment by Region ({sel_year_reg})"
    )
    fig5.update_traces(textposition="top center", marker=dict(sizemin=8), textfont=dict(color="#c9d1d9", size=9))
    fig5.update_layout(**PLOTLY_LAYOUT, height=420, showlegend=False)
    fig5.update_coloraxes(showscale=False)
    st.plotly_chart(fig5, use_container_width=True)

# ════════════════════════════════════════════════════════
# TAB 3 — ISLAND GROUPS
# ════════════════════════════════════════════════════════
with tab3:
    st.markdown("<div class='section-header'>Island Group Performance Over Time</div>", unsafe_allow_html=True)

    isl = df.groupby(["Year", "Island_Group"])[["Unemployment_Rate", "Underemployment_Rate", "LFPR"]].mean().reset_index()

    fig6 = px.line(
        isl, x="Year", y="Unemployment_Rate", color="Island_Group",
        markers=True,
        color_discrete_map={"Luzon": "#388bfd", "Visayas": "#3fb950", "Mindanao": "#d29922"},
        title="Average Unemployment Rate by Island Group (2019–2024)"
    )
    fig6.update_traces(line=dict(width=2.5), marker=dict(size=7))
    fig6.update_layout(**PLOTLY_LAYOUT, height=380)
    st.plotly_chart(fig6, use_container_width=True)

    col_x, col_y = st.columns(2)
    with col_x:
        fig7 = px.bar(
            isl, x="Year", y="Underemployment_Rate", color="Island_Group",
            barmode="group",
            color_discrete_map={"Luzon": "#388bfd", "Visayas": "#3fb950", "Mindanao": "#d29922"},
            title="Underemployment Rate by Island Group"
        )
        fig7.update_layout(**PLOTLY_LAYOUT, height=320)
        st.plotly_chart(fig7, use_container_width=True)

    with col_y:
        # Recovery speed: 2020 Q2 vs 2024 Q2
        recovery = df[df["Quarter"].isin(["Q2"])].groupby(["Year", "Island_Group"])["Unemployment_Rate"].mean().reset_index()
        fig8 = px.line(
            recovery, x="Year", y="Unemployment_Rate", color="Island_Group",
            markers=True,
            color_discrete_map={"Luzon": "#388bfd", "Visayas": "#3fb950", "Mindanao": "#d29922"},
            title="Q2 Unemployment — COVID Recovery by Island Group"
        )
        fig8.update_layout(**PLOTLY_LAYOUT, height=320)
        st.plotly_chart(fig8, use_container_width=True)

# ════════════════════════════════════════════════════════
# TAB 4 — INSIGHTS
# ════════════════════════════════════════════════════════
with tab4:
    st.markdown("<div class='section-header'>Data Insights — What • Why • Action</div>", unsafe_allow_html=True)

    insights = [
        {
            "tag": "Insight 1 · Temporal",
            "title": "COVID-19 Tripled National Unemployment in a Single Quarter",
            "body": (
                "Q2 2020 saw the national average unemployment rate spike from ~5% to over 14%, "
                "representing the sharpest single-quarter increase recorded in the PSA LFS dataset. "
                "Regions under strict community quarantine — particularly NCR and CALABARZON — "
                "recorded rates exceeding 19–22%, reflecting the immediate labor market collapse "
                "caused by non-essential industry shutdowns."
            ),
            "action": "→ Action: DOLE should institutionalize a rapid-response employment fund activated automatically when national unemployment exceeds 10% for two consecutive quarters."
        },
        {
            "tag": "Insight 2 · Regional Disparity",
            "title": "CALABARZON Consistently Leads in Unemployment; BARMM Stays Lowest — a Paradox",
            "body": (
                "Despite being the country's second largest economy, CALABARZON has the highest "
                "unemployment rate across nearly every year in the dataset (5.2–7.9%). This is driven by "
                "a large formal-sector labor force with higher job search expectations. BARMM, conversely, "
                "records the lowest unemployment (1.3–2.9%) but the highest underemployment (22–29%), "
                "revealing a 'hidden unemployment' problem: workers are employed, but not enough."
            ),
            "action": "→ Action: Regional labor policy must be differentiated. CALABARZON needs job-matching and skills programs; BARMM needs quality-of-employment and livelihood intensification programs."
        },
        {
            "tag": "Insight 3 · Structural",
            "title": "Underemployment Has Not Recovered as Fast as Unemployment",
            "body": (
                "While unemployment rates returned to near-pre-COVID levels by 2022–2023, underemployment "
                "rates remain 3–5 percentage points above 2019 baselines in most regions. This divergence "
                "signals that job recovery has been quantity-led, not quality-led: more people are employed, "
                "but many work fewer hours or earn below their capacity. Mindanao regions show the most "
                "persistent underemployment gap."
            ),
            "action": "→ Action: DOLE's labor market success metrics should prioritize underemployment reduction, not just employment rate, as a KPI for regional offices."
        },
        {
            "tag": "Insight 4 · Recovery Speed",
            "title": "Luzon Recovered Faster Than Visayas and Mindanao Post-COVID",
            "body": (
                "By Q4 2021, Luzon's average unemployment had returned to within 1.5pp of 2019 levels, "
                "while Visayas and Mindanao still lagged 2–3pp behind. This faster recovery is attributable "
                "to Luzon's higher concentration of industries that transitioned to remote work (BPO, finance, "
                "tech services), compared to the more agriculture- and tourism-dependent economies of Visayas "
                "and Mindanao."
            ),
            "action": "→ Action: Invest in digital infrastructure and BPO expansion in Visayas and Mindanao to replicate Luzon's resilience model in future economic shocks."
        },
    ]

    for ins in insights:
        st.markdown(f"""<div class='insight-card'>
            <div class='insight-tag'>{ins['tag']}</div>
            <div class='insight-title'>{ins['title']}</div>
            <div class='insight-body'>{ins['body']}</div>
            <div class='insight-action'>{ins['action']}</div>
        </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# TAB 5 — RECOMMENDATIONS
# ════════════════════════════════════════════════════════
with tab5:
    st.markdown("<div class='section-header'>Recommendations for DOLE</div>", unsafe_allow_html=True)

    recs = [
        {
            "n": "01",
            "title": "Establish a COVID-Triggered Emergency Employment Reserve Fund",
            "body": "Create a pre-funded labor buffer that auto-activates when national unemployment crosses a defined threshold. The fund should finance wage subsidies, TUPAD-style programs, and skills bridging for displaced workers — eliminating the 3–6 month policy lag observed during 2020."
        },
        {
            "n": "02",
            "title": "Redesign Regional KPIs to Include Underemployment as a Primary Metric",
            "body": "Current LFS reporting focuses on employment rate. The data shows that underemployment — particularly in BARMM (22–29%) and Mindanao regions — remains critically elevated even when employment looks healthy. DOLE regional offices should be evaluated on underemployment reduction alongside employment rate targets."
        },
        {
            "n": "03",
            "title": "Target CALABARZON for Skills-Matching Programs",
            "body": "CALABARZON's persistently high unemployment (5–8%) in a region with high industrial activity suggests a skills-demand mismatch, not a shortage of jobs. DOLE should partner with CALABARZON's manufacturing, logistics, and semiconductor sectors to design targeted TESDA training pipelines aligned with actual vacancies."
        },
        {
            "n": "04",
            "title": "Accelerate BPO and Digital Economy Expansion to Visayas and Mindanao",
            "body": "Luzon's faster COVID recovery is largely attributable to remote-work-compatible industries. DOLE, DTI, and DICT should jointly incentivize BPO and tech-sector establishment in Visayas and Mindanao through fiscal packages, fiber internet investment, and training hubs to reduce inter-island employment resilience gaps."
        },
    ]

    for rec in recs:
        st.markdown(f"""<div class='rec-card'>
            <div class='rec-number'>#{rec['n']}</div>
            <div class='rec-title'>{rec['title']}</div>
            <div class='rec-body'>{rec['body']}</div>
        </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# TAB 6 — LIMITATIONS
# ════════════════════════════════════════════════════════
with tab6:
    st.markdown("<div class='section-header'>Data Limitations & Honest Caveats</div>", unsafe_allow_html=True)

    limits = [
        "⚠️ Not all quarters are available for all years. 2019 has Q1–Q2 only; 2021 has Q1 and Q4. Quarterly averages should be interpreted with caution.",
        "⚠️ The PSA LFS uses household self-reporting. Informal workers and unregistered businesses may be misclassified as 'employed' even if underemployed or unpaid.",
        "⚠️ BARMM data prior to 2019 has known quality issues due to the region's reorganization. Long-term BARMM trend analysis is limited.",
        "⚠️ Underemployment figures rely on respondent self-assessment of wanting more hours/work. This is subjective and may undercount actual underemployment.",
        "⚠️ COVID-period data (2020–2021) may be affected by survey non-response bias as lockdowns limited field data collection. PSA applied imputation in some quarters.",
        "⚠️ This dataset does not include wage levels, industry breakdowns, or age/sex disaggregation — analysis is limited to regional and temporal patterns.",
    ]

    for lim in limits:
        st.markdown(f"<div class='limit-card'>{lim}</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>Data Cleaning Log</div>", unsafe_allow_html=True)
    st.markdown(f"""<div class='rec-card'>
        <div class='rec-body'>
        📁 Rows loaded: <b style='color:#e6edf3'>{cleaning_log['rows_loaded']}</b><br>
        🔁 Duplicates removed: <b style='color:#e6edf3'>{cleaning_log['duplicates_removed']}</b><br>
        📝 Null Notes fields filled: <b style='color:#e6edf3'>{cleaning_log['nulls_filled']}</b><br>
        ✅ Final rows after cleaning: <b style='color:#3fb950'>{cleaning_log['rows_final']}</b><br>
        ➕ Derived columns added: <b style='color:#388bfd'>{', '.join(cleaning_log['columns_added'])}</b>
        </div>
    </div>""", unsafe_allow_html=True)

# ─── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("<p style='color:#484f58;font-size:0.75rem;text-align:center'>Data: PSA Labor Force Survey 2019–2024 · openstat.psa.gov.ph · Stakeholder: DOLE · Capstone Project · Data Analytics Track</p>", unsafe_allow_html=True)
