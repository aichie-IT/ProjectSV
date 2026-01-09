import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------
# Page configuration
# ---------------------------
st.set_page_config(
    page_title="Internet Usage & Mental Health Dashboard",
    layout="wide"
)

st.title("Internet Usage and Mental Health Outcomes")
st.caption("Interactive dashboard for exploring relationships between internet use and mental health indicators")

# ---------------------------
# Load data directly
# ---------------------------
@st.cache_data
def load_data():
    return pd.read_csv(
        "/content/drive/MyDrive/Copy of Exploring Internet Use and Suicidality in Mental Health Populations   (Responses) - Form Responses 1.csv"
    )

df = load_data()

st.success("Dataset loaded successfully")

# ---------------------------
# Sidebar controls
# ---------------------------
with st.sidebar:
    st.header("Variable Selection")

    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    usage_col = st.selectbox("Internet Usage Variable", numeric_cols)
    mental_col = st.selectbox("Mental Health Outcome Variable", numeric_cols)
    filter_col = st.selectbox("Filter Variable", numeric_cols)

# ---------------------------
# Slider filter
# ---------------------------
min_val, max_val = df[filter_col].min(), df[filter_col].max()

value_range = st.sidebar.slider(
    f"Select range for {filter_col}",
    float(min_val),
    float(max_val),
    (float(min_val), float(max_val))
)

filtered_df = df[
    (df[filter_col] >= value_range[0]) &
    (df[filter_col] <= value_range[1])
]

# ---------------------------
# Layout
# ---------------------------
col1, col2 = st.columns(2)

# ---------------------------
# Scatter plot
# ---------------------------
with col1:
    st.subheader("Relationship Between Internet Usage and Mental Health")
    fig1 = px.scatter(
        filtered_df,
        x=usage_col,
        y=mental_col,
        trendline="ols",
        hover_data=filtered_df.columns
    )
    st.plotly_chart(fig1, use_container_width=True)

# ---------------------------
# Histogram
# ---------------------------
with col2:
    st.subheader("Distribution of Mental Health Outcomes")
    fig2 = px.histogram(
        filtered_df,
        x=mental_col,
        nbins=20
    )
    st.plotly_chart(fig2, use_container_width=True)

# ---------------------------
# Summary stats
# ---------------------------
st.subheader("Summary Statistics")
st.dataframe(filtered_df[[usage_col, mental_col]].describe())
