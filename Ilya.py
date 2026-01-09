import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Internet Usage and Mental Health Outcomes")
st.caption("Interactive visualization adapted from Colab analysis")

# Upload CSV
uploaded_file = st.file_uploader("Upload Google Form CSV", type="csv")

if uploaded_file is None:
    st.warning("Please upload the dataset to continue.")
    st.stop()

# Load data
df = pd.read_csv(uploaded_file, encoding="latin-1")

st.success("Dataset loaded successfully")

# Sidebar controls
with st.sidebar:
    st.header("Controls")

    mental_factor = st.selectbox(
        "Mental Health Factor",
        df["Mental_Health_Factor"].unique()
    )

    usage_range = st.slider(
        "Daily Internet Usage (Hours)",
        float(df["Daily_Internet_Usage_Hours"].min()),
        float(df["Daily_Internet_Usage_Hours"].max()),
        (
            float(df["Daily_Internet_Usage_Hours"].min()),
            float(df["Daily_Internet_Usage_Hours"].max())
        )
    )

# Filter data
filtered_df = df[
    (df["Mental_Health_Factor"] == mental_factor) &
    (df["Daily_Internet_Usage_Hours"] >= usage_range[0]) &
    (df["Daily_Internet_Usage_Hours"] <= usage_range[1])
]

# Layout
col1, col2 = st.columns(2)

# Scatter plot (MAIN visualization)
with col1:
    st.subheader("Internet Usage vs Mental Health Score")
    fig1 = px.scatter(
        filtered_df,
        x="Daily_Internet_Usage_Hours",
        y="Score",
        trendline="ols",
        hover_data=filtered_df.columns
    )
    st.plotly_chart(fig1, use_container_width=True)

# Distribution
with col2:
    st.subheader("Score Distribution")
    fig2 = px.histogram(
        filtered_df,
        x="Score",
        nbins=15
    )
    st.plotly_chart(fig2, use_container_width=True)

# Summary
st.subheader("Summary Statistics")
st.dataframe(filtered_df.describe())


