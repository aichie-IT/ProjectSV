import pandas as pd
import plotly.express as px
import streamlit as st

# --- LOAD DATA ---
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQnrGG72xRS-qLoiM2zon4eP8t5XMiO5MhoLUEe2jJer0G5EzodiU4e0NOmx_ssmCwZf-AnbQXhBbTM/pub?gid=1791189796&single=true&output=csv"
    return pd.read_csv(url)

df = load_data()

# Re-apply short label mapping to 'Social_Media_Use_Frequency'
short_label_map_for_df = {
    "Less than 1 hour per day": "< 1 hr",
    "1 to 2 hours per day": "1–2 hrs",
    "3 to 4 hours per day": "3–4 hrs",
    "5 to 6 hours per day": "5–6 hrs",
    "More than 6 hours per day": "> 6 hrs"
}
df["Social_Media_Use_Frequency"] = df["Social_Media_Use_Frequency"].map(short_label_map_for_df)

# Create df_for_analysis by dropping the 'Platforms_Most_Often_Used' column
df_for_analysis = df.drop(columns=['Platforms_Most_Often_Used']).copy()

# Define numerical mapping for Social Media Use Frequency
social_media_hours_map = {
    "< 1 hr": 0.5,
    "1–2 hrs": 1.5,
    "3–4 hrs": 3.5,
    "5–6 hrs": 5.5,
    "> 6 hrs": 7
}
df_for_analysis["Daily_Internet_Usage_Hours"] = df_for_analysis["Social_Media_Use_Frequency"].map(social_media_hours_map)

# Define mental health related columns and convert them to numeric
mental_health_cols = [
    'Assignments_Stress',
    'Academic_Workload_Anxiety',
    'Difficulty_Sleeping_University_Pressure',
    'Social_Media_Negative_Impact_on_Wellbeing'
]

for col in mental_health_cols:
    df_for_analysis[col] = pd.to_numeric(df_for_analysis[col])

# Map mental health factor names for better legend readability
mental_health_factor_map = {
    'Assignments_Stress': 'Stress from Assignments',
    'Academic_Workload_Anxiety': 'Academic Workload Anxiety',
    'Difficulty_Sleeping_University_Pressure': 'Difficulty Sleeping (Pressure)',
    'Social_Media_Negative_Impact_on_Wellbeing': 'Negative Social Media Impact'
}

df_for_analysis['Mental_Health_Factor'] = df_for_analysis[mental_health_cols].apply(
    lambda row: mental_health_factor_map.get(row.name), axis=1
)

# Melt the DataFrame for easier plotting with Plotly
df_melted = df_for_analysis.melt(
    id_vars=['Daily_Internet_Usage_Hours'],
    value_vars=mental_health_cols,
    var_name='Mental_Health_Factor',
    value_name='Score'
)

df_melted['Mental_Health_Factor'] = df_melted['Mental_Health_Factor'].map(mental_health_factor_map)

# Group by internet usage and mental health factor, then calculate the mean score
df_grouped = df_melted.groupby(['Daily_Internet_Usage_Hours', 'Mental_Health_Factor'])['Score'].mean().reset_index()

# Create Plotly grouped bar chart
fig = px.bar(
    df_grouped,
    x='Daily_Internet_Usage_Hours',
    y='Score',
    color='Mental_Health_Factor',
    barmode='group',
    labels={'Daily_Internet_Usage_Hours': 'Internet Usage (hours)', 'Score': 'Mental Health Score'},
    title="Mental Health Scores by Internet Usage"
)

# Display Plotly chart in Streamlit
st.plotly_chart(fig)

# --- Box Plot ---
# Create the box plot for "Difficulty Sleeping Due to University Pressure by Social Media Affecting Sleep"
df_new = df.copy() # Re-load original dataset
df_new['Sleep_Affected_By_Social_Media_Numeric_Str'] = df_new['Sleep_Affected_By_Social_Media'].astype(str)

def map_sleep_impact_to_binary(response_str):
    try:
        response_int = int(response_str)
        if response_int >= 4: # Assuming 4 (Agree) and 5 (Strongly Agree) mean 'Yes'
            return 'Yes'
        elif response_int <= 3: # Assuming 1 (Strongly Disagree), 2 (Disagree), 3 (Neutral) mean 'No'
            return 'No'
    except ValueError: # Handle cases where conversion to int fails (e.g., non-numeric data)
        return None

df_new['Internet_Use_Affects_Sleep'] = df_new['Sleep_Affected_By_Social_Media_Numeric_Str'].apply(map_sleep_impact_to_binary)

df_new['Difficulty_Sleeping_University_Pressure_Numeric_Str'] = df_new['Difficulty_Sleeping_University_Pressure'].astype(str)
df_new['Difficulty_Sleeping_University_Pressure_Score'] = df_new['Difficulty_Sleeping_University_Pressure_Numeric_Str'].map(likert_numeric_map)

df_plot = df_new.dropna(subset=['Internet_Use_Affects_Sleep', 'Difficulty_Sleeping_University_Pressure_Score']).copy()

fig_box = px.box(
    df_plot,
    x='Internet_Use_Affects_Sleep',
    y='Difficulty_Sleeping_University_Pressure_Score',
    points="all",
    labels={'Difficulty_Sleeping_University_Pressure_Score': 'Difficulty Sleeping Score'},
    title='Difficulty Sleeping Due to University Pressure by Social Media Affecting Sleep'
)

st.plotly_chart(fig_box)

# --- Heatmap ---
# Create correlation heatmap
numerical_cols = ['Age', 'Social_Media_Hours_Numeric', 'Study_Hours_Numeric'] + \
                 [col for col in likert_cols if col in df_heatmap.columns and df_heatmap[col].dtype != 'object']

correlation_matrix = df_heatmap[numerical_cols].dropna().corr()

fig_heatmap = px.imshow(
    correlation_matrix,
    labels=dict(x="Variables", y="Variables", color="Correlation"),
    title="Correlation Heatmap"
)

st.plotly_chart(fig_heatmap)

# --- Line Plot ---
df_grouped_line = df_melted.groupby(['Daily_Internet_Usage_Hours', 'Mental_Health_Factor'])['Score'].mean().reset_index()

fig_line = px.line(
    df_grouped_line,
    x='Daily_Internet_Usage_Hours',
    y='Score',
    color='Mental_Health_Factor',
    line_shape='linear',
    title="Mental Health Scores vs Internet Usage"
)

st.plotly_chart(fig_line)



