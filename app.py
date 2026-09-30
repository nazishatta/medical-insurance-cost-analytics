"""Medical Insurance Cost Explorer | Streamlit application."""

from __future__ import annotations

import math
from pathlib import Path

import plotly.express as px
import streamlit as st
import pandas as pd

from analytics import (
    SMOKER_LABELS,
    filter_insurance_data,
    region_summary,
    validate_insurance_data,
)

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "insurance.csv"

BACKGROUND = "#111318"
PANEL = "#1b2028"
TEXT = "#e9eff4"
MUTED = "#abb6c4"
TEAL = "#6cdec9"
AMBER = "#f5b76b"
SMOKER_COLORS = {"Non-smoker": TEAL, "Smoker": AMBER}

st.set_page_config(
    page_title="Medical Insurance Cost Explorer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data(show_spinner="Preparing insurance data…")
def load_data(file_path: str, file_mtime_ns: int) -> pd.DataFrame:
    """Read and validate the bundled CSV only when its content may have changed.

    Including the file modification timestamp in the cache key means local data
    revisions invalidate cached results without disabling caching on widget reruns.
    """
    _ = file_mtime_ns
    return validate_insurance_data(pd.read_csv(file_path))


def style_chart(fig, height: int = 370):
    """Apply one restrained high-contrast visual identity to every chart."""
    fig.update_layout(
        template="plotly_dark",
        height=height,
        paper_bgcolor=PANEL,
        plot_bgcolor=PANEL,
        font=dict(color=TEXT, family="Arial, sans-serif", size=12),
        margin=dict(l=12, r=18, t=26, b=12),
        legend=dict(title=None, orientation="h", yanchor="bottom", y=1.01, x=0),
        hoverlabel=dict(bgcolor="#252c36", font_color=TEXT),
    )
    fig.update_xaxes(gridcolor="#343b45", zerolinecolor="#343b45")
    fig.update_yaxes(gridcolor="#343b45", zerolinecolor="#343b45")
    return fig


st.markdown(
    """
    <style>
      .block-container {padding-top: 2.2rem; padding-bottom: 2rem; max-width: 1460px;}
      .hero {
        border: 1px solid #343b46; border-radius: 18px;
        padding: 27px 30px 22px;
        background: linear-gradient(110deg, #202832 0%, #171b22 68%, #14181e 100%);
        margin-bottom: 21px;
      }
      .hero .eyebrow {
        font-size: 0.78rem; font-weight: 700; letter-spacing: 0.15em;
        text-transform: uppercase; color: #79e6d1;
      }
      .hero h1 {
        color: #f0f4f7; font-size: clamp(1.8rem, 3vw, 2.75rem);
        line-height: 1.15; margin: 10px 0 12px;
      }
      .hero p {color: #b8c4d0; max-width: 780px; line-height: 1.6; margin: 0;}
      .analysis-note {
        color: #b8c4d0; font-size: 0.89rem; margin-top: 8px;
      }
      [data-testid="stMetric"] {
        background: #1b2028; border: 1px solid #343b46;
        padding: 17px 19px; border-radius: 14px;
      }
      [data-testid="stMetricLabel"] {color: #b8c4d0;}
      [data-testid="stMetricValue"] {color: #f1f6f9;}
      div[data-testid="stSidebarContent"] {border-right: 1px solid #323a44;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">Healthcare analytics / Interactive explorer</div>
      <h1>Medical Insurance Cost Explorer</h1>
      <p>Discover how recorded medical charges vary across age, BMI, smoking
      status and U.S. regions. Refine the population, inspect the visual
      patterns and export the exact records behind the charts.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if not DATA_FILE.is_file():
    st.error("Missing data/insurance.csv. Keep the dataset in the repository's data folder.")
    st.stop()

try:
    data = load_data(str(DATA_FILE), DATA_FILE.stat().st_mtime_ns)
except (OSError, ValueError, pd.errors.ParserError) as error:
    st.error(f"Unable to load the insurance data: {error}")
    st.stop()

st.sidebar.markdown("## Explore the data")
st.sidebar.caption("Filters update all metrics, charts and the exported CSV.")

smoker_options = list(SMOKER_LABELS.values())
selected_smoker_labels = st.sidebar.multiselect(
    "Smoking status", options=smoker_options, default=smoker_options
)
selected_smokers = [
    raw for raw, display in SMOKER_LABELS.items()
    if display in selected_smoker_labels
]

regions = sorted(data["region"].unique().tolist())
region_labels = {r.title(): r for r in regions}
selected_region_labels = st.sidebar.multiselect(
    "Region", options=list(region_labels), default=list(region_labels)
)
selected_regions = [region_labels[label] for label in selected_region_labels]

age_min = int(data["age"].min())
age_max = int(data["age"].max())
selected_ages = st.sidebar.slider(
    "Age (years)", age_min, age_max, (age_min, age_max)
)

bmi_min = math.floor(float(data["bmi"].min()) * 2) / 2
bmi_max = math.ceil(float(data["bmi"].max()) * 2) / 2
selected_bmi = st.sidebar.slider(
    "BMI", bmi_min, bmi_max, (bmi_min, bmi_max), step=0.5
)

st.sidebar.divider()
region_stat = st.sidebar.radio(
    "Regional comparison metric", ["Mean", "Median"], horizontal=True
)
st.sidebar.caption("Tip: choose one smoking group to inspect its distribution separately.")

filtered = filter_insurance_data(
    data, selected_ages, selected_bmi, selected_smokers, selected_regions
)

st.caption(f"EXPLORING {len(filtered):,} OF {len(data):,} RECORDS · FILTERS APPLY TO EVERY VIEW")

if filtered.empty:
    st.warning("No records match the current filters. Broaden your age/BMI ranges or select more groups.")
    st.stop()

metric_1, metric_2, metric_3, metric_4 = st.columns(4, gap="medium")
metric_1.metric("Records", f"{len(filtered):,}")
metric_2.metric("Mean charges", f"{filtered['charges'].mean():,.0f}")
metric_3.metric("Median charges", f"{filtered['charges'].median():,.0f}")
metric_4.metric("Smoker share", f"{filtered['smoker'].eq('yes').mean():.1%}")

st.markdown(
    '<div class="analysis-note">Charges are presented in the dataset\'s supplied units; '
    'the CSV does not independently document currency, time period or billing methodology.</div>',
    unsafe_allow_html=True,
)

chart_tab, data_tab, about_tab = st.tabs(
    ["📈  Visualizations", "▦  Data & export", "ⓘ  About"]
)

with chart_tab:
    st.markdown("### Exploring individual charges")
    st.caption("Each point represents one CSV record. Colors identify smoking status; hover for more detail.")

    plot_data = filtered.copy()
    plot_data["Smoking status"] = plot_data["smoker"].map(SMOKER_LABELS)
    plot_data["Region"] = plot_data["region"].str.title()

    left, right = st.columns(2, gap="medium")

    with left:
        st.markdown("**Age and charges**")
        age_fig = px.scatter(
            plot_data,
            x="age", y="charges", color="Smoking status",
            color_discrete_map=SMOKER_COLORS,
            category_orders={"Smoking status": smoker_options},
            labels={"age": "Age (years)", "charges": "Charges (dataset units)"},
            hover_data={"bmi": ":.2f", "Region": True, "children": True},
            opacity=0.77,
        )
        age_fig.update_traces(marker=dict(size=8, line=dict(width=0)))
        age_fig.update_yaxes(tickformat=",.0f", rangemode="tozero")
        st.plotly_chart(style_chart(age_fig), use_container_width=True, config={"displaylogo": False})
        st.caption("Position encodes age and charges; hue distinguishes smoking groups.")

    with right:
        st.markdown("**BMI and charges**")
        bmi_fig = px.scatter(
            plot_data,
            x="bmi", y="charges", color="Smoking status",
            color_discrete_map=SMOKER_COLORS,
            category_orders={"Smoking status": smoker_options},
            labels={"bmi": "Body mass index (BMI)", "charges": "Charges (dataset units)"},
            hover_data={"age": True, "Region": True, "children": True},
            opacity=0.77,
        )
        bmi_fig.update_traces(marker=dict(size=8, line=dict(width=0)))
        bmi_fig.update_yaxes(tickformat=",.0f", rangemode="tozero")
        st.plotly_chart(style_chart(bmi_fig), use_container_width=True, config={"displaylogo": False})
        st.caption("The same charge scale allows comparisons across both scatter plots.")

    st.divider()
    st.markdown(f"### Regional comparison · {region_stat.lower()} charges")
    st.caption("Region-level summary for the selected records, not the unfiltered dataset.")
    aggregated = region_summary(filtered, region_stat)
    region_fig = px.bar(
        aggregated, x="region_label", y="charge_value",
        text="charge_value", custom_data=["observations"],
        labels={"region_label": "Region", "charge_value": f"{region_stat} charges (dataset units)"},
    )
    region_fig.update_traces(
        marker_color=TEAL,
        texttemplate="%{text:,.0f}", textposition="outside",
        hovertemplate="%{x}<br>Charges: %{y:,.2f}<br>Records: %{customdata[0]:,}<extra></extra>",
    )
    region_fig.update_yaxes(rangemode="tozero", tickformat=",.0f")
    region_fig.update_layout(showlegend=False, bargap=0.42, margin=dict(l=12, r=18, t=30, b=12))
    st.plotly_chart(style_chart(region_fig, height=340), use_container_width=True, config={"displaylogo": False})
    st.info("These are descriptive associations in the available sample, not evidence that a characteristic causes higher charges.")

with data_tab:
    st.markdown("### Inspect and export the selected records")
    st.caption(f"{len(filtered):,} rows · {filtered.shape[1]} original columns · all sidebar filters applied")
    st.dataframe(filtered.reset_index(drop=True), use_container_width=True, hide_index=True, height=420)
    export_csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇ Download filtered CSV",
        data=export_csv,
        file_name="medical_insurance_filtered.csv",
        mime="text/csv",
        type="primary",
    )
    st.caption("Export retains original column names and source-level observations, including any identical rows.")

with about_tab:
    st.markdown("### About the data")
    st.write(
        "This explorer uses a bundled, seven-column insurance-cost CSV. "
        "Each row contains age, recorded sex, BMI, number of children, smoking status, "
        "U.S. region and a numerical charges field. "
        "The original file does not include dates, insurer identifiers or plan-level details."
    )
    quality_left, quality_right, quality_third = st.columns(3)
    quality_left.metric("Source records", f"{len(data):,}")
    quality_right.metric("Missing cells", f"{int(data.isna().sum().sum()):,}")
    quality_third.metric("Exact duplicate rows", f"{int(data.duplicated().sum()):,}")
    st.caption("All source rows are retained; no record is silently dropped or imputed.")

    with st.expander("Data dictionary", expanded=True):
        dictionary = pd.DataFrame(
            [
                ("age", "Age, in years"),
                ("sex", "Recorded sex category"),
                ("bmi", "Body mass index"),
                ("children", "Recorded number of covered children/dependents"),
                ("smoker", "Smoking status: yes / no"),
                ("region", "Recorded U.S. region"),
                ("charges", "Numerical medical-cost charges field"),
            ],
            columns=["Column", "Interpretation"],
        )
        st.dataframe(dictionary, hide_index=True, use_container_width=True)

    st.markdown("### How to read the charts")
    st.write(
        "The scatter plots use a shared quantitative vertical scale and distinct color categories. "
        "The bar chart starts at zero and aggregates only the records selected in the sidebar. "
        "Mean and median can differ when a distribution is skewed."
    )
    st.markdown("### Interpretation limits")
    st.write(
        "The CSV alone does not establish sampling representativeness, currency, collection date, "
        "causality or current insurance pricing. Treat comparisons as exploratory descriptions "
        "of these 1,338 records, not individual medical or financial advice."
    )

st.divider()
st.caption("MEDICAL INSURANCE COST EXPLORER · Python / Pandas / Plotly / Streamlit")
