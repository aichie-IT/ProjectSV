import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Internet Usage and Mental Health Outcomes")
st.caption("Interactive visualization adapted from Colab analysis")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQnrGG72xRS-qLoiM2zon4eP8t5XMiO5MhoLUEe2jJer0G5EzodiU4e0NOmx_ssmCwZf-AnbQXhBbTM/pub?gid=1791189796&single=true&output=csv"
    return pd.read_csv(url)

df = load_data()

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

# Layout: 2 rows, 2 columns for first 4 plots, 1 row for 5th
col1, col2 = st.columns(2)

# 1️⃣ Scatter plot with trendline
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

# 2️⃣ Histogram / Distribution
with col2:
    st.subheader("Score Distribution")
    fig2 = px.histogram(
        filtered_df,
        x="Score",
        nbins=15,
        color_discrete_sequence=["indianred"]
    )
    st.plotly_chart(fig2, use_container_width=True)

# 3️⃣ Box plot: show distribution by internet usage categories
col3, col4 = st.columns(2)
with col3:
    st.subheader("Score by Internet Usage Category")
    # Optional: create categories
    bins = [0, 2, 4, 6, 8, 24]
    labels = ["0-2h", "2-4h", "4-6h", "6-8h", "8+h"]
    filtered_df["Usage_Category"] = pd.cut(filtered_df["Daily_Internet_Usage_Hours"], bins=bins, labels=labels)
    
    fig3 = px.box(
        filtered_df,
        x="Usage_Category",
        y="Score",
        color="Usage_Category"
    )
    st.plotly_chart(fig3, use_container_width=True)

# 4️⃣ Correlation heatmap
with col4:
    st.subheader("Correlation Heatmap")
    corr_df = filtered_df[["Daily_Internet_Usage_Hours", "Score"]].corr()
    fig4 = px.imshow(
        corr_df,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        zmin=-1, zmax=1
    )
    st.plotly_chart(fig4, use_container_width=True)

# 5️⃣ Violin plot: detailed score distribution by category
st.subheader("Score Distribution by Internet Usage Category")
fig5 = px.violin(
    filtered_df,
    x="Usage_Category",
    y="Score",
    color="Usage_Category",
    box=True,
    points="all"
)
st.plotly_chart(fig5, use_container_width=True)

# Summary
st.subheader("Summary Statistics")
st.dataframe(filtered_df.describe())



