import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Internet Usage and Mental Health Outcomes")
st.caption("Interactive Streamlit dashboard")

# Upload CSV
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is None:
    st.warning("Please upload the dataset to continue.")
    st.stop()

# Load data
df = pd.read_csv(uploaded_file)

st.success("Dataset loaded successfully")

# Keep ONLY numeric columns
numeric_cols = df.select_dtypes(include="number").columns.tolist()

if len(numeric_cols) < 2:
    st.error("Dataset must contain at least two numeric columns.")
    st.stop()

# Sidebar controls
with st.sidebar:
    st.header("Controls")
    usage_col = st.selectbox("Internet Usage Variable", numeric_cols)
    mental_col = st.selectbox("Mental Health Variable", numeric_cols)
    filter_col = st.selectbox("Filter Variable", numeric_cols)

    min_val = float(df[filter_col].min())
    max_val = float(df[filter_col].max())

    value_range = st.slider(
        "Filter range",
        min_val,
        max_val,
        (min_val, max_val)
    )

# Filter data
filtered_df = df[
    (df[filter_col] >= value_range[0]) &
    (df[filter_col] <= value_range[1])
]

# Layout
col1, col2 = st.columns(2)

# Scatter plot
with col1:
    fig1 = px.scatter(
        filtered_df,
        x=usage_col,
        y=mental_col,
        trendline="ols",
        title="Internet Usage vs Mental Health",
        hover_data=filtered_df.columns
    )
    st.plotly_chart(fig1, use_container_width=True)

# Histogram
with col2:
    fig2 = px.histogram(
        filtered_df,
        x=mental_col,
        nbins=20,
        title="Distribution of Mental Health Outcomes"
    )
    st.plotly_chart(fig2, use_container_width=True)

# Summary
st.subheader("Summary Statistics")
st.dataframe(filtered_df[[usage_col, mental_col]].describe())

