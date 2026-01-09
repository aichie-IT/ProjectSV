import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------
# Page configuration
# ---------------------------
st.set_page_config(
    page_title="Internet Usage & Mental Health Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Internet Usage and Mental Health Outcomes")
st.caption("Interactive dashboard for exploring relationships between internet use and mental health indicators")

# ---------------------------
# Data loading
# ---------------------------
@st.cache_data
def load_data(file):
    return pd.read_csv(file)

with st.sidebar:
    st.header("Data Controls")
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is None:
    st.info("/content/drive/MyDrive/Copy of Exploring Internet Use and Suicidality in Mental Health Populations   (Responses) - Form Responses 1.csv"
           )
    st.stop()

df = load_data(uploaded_file)

# ---------------------------
# Column selection
# ---------------------------
with st.sidebar:
    st.subheader("Variable Selection")
    usage_col = st.selectbox("Internet Usage Variable", df.columns)
    mental_col = st.selectbox("Mental Health Outcome Variable", df.columns)
    
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    filter_col = st.selectbox("Filter Variable (numeric)", numeric_cols)

# ---------------------------
# Filters & sliders
# ---------------------------
min_val, max_val = float(df[filter_col].min()), float(df[filter_col].max())

with st.sidebar:
    st.subheader("Filters")
    value_range = st.slider(
        f"Select range for {filter_col}",
        min_value=min_val,
        max_value=max_val,
        value=(min_val, max_val)
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
# Visualization 1: Scatter plot
# ---------------------------
with col1:
    st.subheader("Relationship Between Variables")
    scatter_fig = px.scatter(
        filtered_df,
        x=usage_col,
        y=mental_col,
        hover_data=filtered_df.columns,  # tooltips
        trendline="ols",
        title=f"{usage_col} vs {mental_col}"
    )
    st.plotly_chart(scatter_fig, use_container_width=True)

# ---------------------------
# Visualization 2: Distribution
# ---------------------------
with col2:
    st.subheader("Distribution of Mental Health Outcomes")
    hist_fig = px.histogram(
        filtered_df,
        x=mental_col,
        nbins=20,
        title=f"Distribution of {mental_col}"
    )
    st.plotly_chart(hist_fig, use_container_width=True)

# ---------------------------
# Summary statistics
# ---------------------------
st.subheader("Summary Statistics")
st.dataframe(filtered_df[[usage_col, mental_col]].describe())

# ---------------------------
# Footer
# ---------------------------
st.markdown(
    """
    ---
    **Features included:** filters, sliders, interactive tooltips, dynamic visualizations.  
    Designed for clear interpretation by both technical and non-technical users.
    """
)

