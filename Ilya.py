import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

px.defaults.template = "plotly_white"
px.defaults.color_continuous_scale = px.colors.sequential.Teal

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Internet Use and Mental Health Dashboard",
    page_icon="🧠",
    layout="wide"
)

# --- LOAD DATA ---
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQnrGG72xRS-qLoiM2zon4eP8t5XMiO5MhoLUEe2jJer0G5EzodiU4e0NOmx_ssmCwZf-AnbQXhBbTM/pub?gid=1791189796&single=true&output=csv"
    return pd.read_csv(url)

df = load_data()

# Clean Column Names
df.columns = df.columns.str.strip()
# --- PLOT ---
fig = px.bar(
    df_melted,
    x="Internet_Usage_Category",
    y="Score",
    color="Mental_Health_Factor",
    barmode="group",
    category_orders={"Internet_Usage_Category": order},
    labels={
        "Score": "Mean Score (Likert Scale: 1–5)",
        "Internet_Usage_Category": "Internet Usage Category",
        "Mental_Health_Factor": "Mental Health Factor"
    }
)

fig.update_layout(
    title="Average Mental Health Scores by Internet Usage Level",
    legend_title_text="Mental Health Factor",
    height=600
)

st.plotly_chart(fig, use_container_width=True)
