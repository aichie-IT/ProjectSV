import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# ==============================
# LOAD DATA
# ==============================
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQnrGG72xRS-qLoiM2zon4eP8t5XMiO5MhoLUEe2jJer0G5EzodiU4e0NOmx_ssmCwZf-AnbQXhBbTM/pub?gid=1791189796&single=true&output=csv"
    return pd.read_csv(url)

df = load_data()
df.columns = df.columns.str.strip()

# ==============================
# TITLE & DESCRIPTION
# ==============================
st.title("Relationship Between Internet Usage and Mental Health Outcomes")

st.write("""
This app explores the relationship between internet usage and mental health outcomes
among UMK students, focusing on stress, anxiety, sleep difficulty, and social media impact.
""")

# ==============================
# BOX PLOT
# ==============================
df_new = df.copy()

df_new['Sleep_Affected_By_Social_Media_Numeric_Str'] = (
    df_new['Sleep_Affected_By_Social_Media'].astype(str)
)

def map_sleep_impact_to_binary(response_str):
    try:
        response_int = int(response_str)
        if response_int >= 4:
            return 'Yes'
        elif response_int <= 3:
            return 'No'
    except ValueError:
        return None

df_new['Internet_Use_Affects_Sleep'] = (
    df_new['Sleep_Affected_By_Social_Media_Numeric_Str']
    .apply(map_sleep_impact_to_binary)
)

df_new['Difficulty_Sleeping_University_Pressure_Score'] = pd.to_numeric(
    df_new['Difficulty_Sleeping_University_Pressure'],
    errors='coerce'
)

df_plot = df_new.dropna(subset=[
    'Internet_Use_Affects_Sleep',
    'Difficulty_Sleeping_University_Pressure_Score'
]).copy()

fig_box = px.box(
    df_plot,
    x='Internet_Use_Affects_Sleep',
    y='Difficulty_Sleeping_University_Pressure_Score',
    points="all",
    title='Difficulty Sleeping Due to University Pressure by Social Media Affecting Sleep',
    labels={
        'Internet_Use_Affects_Sleep': 'Social Media Affects Sleep',
        'Difficulty_Sleeping_University_Pressure_Score': 'Difficulty Sleeping Score'
    }
)

st.plotly_chart(fig_box, use_container_width=True)

# ==============================
# LINE PLOT
# ==============================
st.subheader("Daily Internet Usage vs Mean Mental Health Scores")

df_line = df_melted.copy()

df_line["Score"] = pd.to_numeric(df_line["Score"], errors="coerce")
df_line["Daily_Internet_Usage_Hours"] = pd.to_numeric(
    df_line["Daily_Internet_Usage_Hours"], errors="coerce"
)

df_line = df_line.dropna(
    subset=["Score", "Daily_Internet_Usage_Hours", "Mental_Health_Factor"]
)

df_grouped_line = (
    df_line
    .groupby(["Daily_Internet_Usage_Hours", "Mental_Health_Factor"])["Score"]
    .mean()
    .reset_index()
    .sort_values("Daily_Internet_Usage_Hours")
)

df_grouped_line['Daily_Internet_Usage_Hours_Str'] = (
    df_grouped_line['Daily_Internet_Usage_Hours'].astype(str)
)

fig_line = px.line(
    df_grouped_line,
    x='Daily_Internet_Usage_Hours_Str',
    y='Score',
    facet_col='Mental_Health_Factor',
    facet_col_wrap=2,
    markers=True,
    title='Daily Internet Usage vs Mean Mental Health Scores',
    labels={
        'Daily_Internet_Usage_Hours_Str': 'Daily Internet Usage (Hours)',
        'Score': 'Mean Mental Health Score'
    }
)

fig_line.update_layout(template='plotly_white', height=600)
fig_line.update_yaxes(dtick=1)

st.plotly_chart(fig_line, use_container_width=True)

# ==============================
# SCATTER PLOTS (SEABORN)
# ==============================
st.subheader("Scatter Plots: Daily Internet Usage vs Mental Health Scores")

g = sns.relplot(
    x='Daily_Internet_Usage_Hours',
    y='Score',
    col='Mental_Health_Factor',
    col_wrap=2,
    data=df_line,
    kind='scatter',
    height=4,
    aspect=1.2,
    s=50,
    alpha=0.7
)

g.set_axis_labels("Daily Internet Usage (Hours)", "Mental Health Score")
g.set_titles("{col_name}")

plt.tight_layout()
st.pyplot(g.fig)

   
