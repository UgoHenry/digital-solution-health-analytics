import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Digital Solution Dashboard",
    page_icon="🩺",
    layout="wide"
)

st.title("Digital Solution Dashboard")
st.write("Community Hypertension Screening & Triage Portal (US-11)")

# Cached functions to load pre-aggregated tables
@st.cache_data
def load_state_data():
    return pd.read_parquet("data/agg_by_state.parquet")

@st.cache_data
def load_zone_year_data():
    return pd.read_parquet("data/agg_by_zone_year.parquet")

@st.cache_data
def load_age_data():
    return pd.read_parquet("data/agg_by_age_group.parquet")

df_state = load_state_data()
df_zone_year = load_zone_year_data()
df_age = load_age_data()

# Compute top-level metrics from the summary tables
total_surveys = df_state['total_surveys'].sum()
total_hypertensive = df_state['hypertensive_count'].sum()
overall_prevalence = total_hypertensive / total_surveys

col1, col2, col3 = st.columns(3)
col1.metric("Total Surveys", f"{total_surveys:,}")
col2.metric("Hypertensive Cases", f"{total_hypertensive:,}")
col3.metric("Overall Prevalence", f"{overall_prevalence * 100:.2f}%")

st.divider()

# Tabbed view for fast inspection
tab1, tab2, tab3 = st.tabs(["By State", "By Zone & Year", "By Age Group"])

with tab1:
    st.subheader("State-Level Summary")
    st.dataframe(df_state, use_container_width=True)

with tab2:
    st.subheader("Geopolitical Zone & Year Summary")
    st.dataframe(df_zone_year, use_container_width=True)

with tab3:
    st.subheader("Age Group Breakdown")
    st.dataframe(df_age, use_container_width=True)