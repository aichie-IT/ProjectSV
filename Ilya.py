import streamlit as st
import pandas as pd
import plotly.express as px

# --- Load data (already loaded in your earlier code) ---
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQnrGG72xRS-qLoiM2zon4eP8t5XMiO5MhoLUEe2jJer0G5EzodiU4e0NOmx_ssmCwZf-AnbQXhBbTM/pub?gid=1791189796&single=true&output=csv"
    return pd.read_csv(url)

df = load_data()

# Clean Column Names
df.columns = df.columns.str.strip()

# Rename Columns (Already done)
df = df.rename(columns={...})  # Your renaming code goes here

# Ensure that the df_melted dataframe exists and contains 'Internet_Usage_Category', 'Score', and 'Mental_Health_Factor'
# If not, melt the dataframe as you did before.
df_melted = df.melt(
    id_vars=['Internet_Usage_Category'],
    value_vars=['Assignments_Stress', 'Academic_Workload_Anxiety', 'Difficulty_Sleeping_University_Pressure', 'Social_Media_Negative_Impact_on_Wellbeing'],
    var_name='Mental_Health_Factor',
    value_name='Score'
)

# Define the order of the categories
order = ['Low', 'Moderate', 'High']

# Plot the grouped bar chart using Plotly
fig = px.bar(
    df_melted,
    x='Internet_Usage_Category',
    y='Score',
    color='Mental_Health_Factor',
    title='Average Mental Health Scores by Internet Usage Level',
    labels={'Score': 'Mean Score (Likert Scale: 1=Strongly Disagree, 5=Strongly Agree)', 'Internet_Usage_Category': 'Internet Usage Category'},
    category_orders={'Internet_Usage_Category': order},  # Make sure the order of categories is correct
    barmode='group',  # This creates the grouped bar chart
)

# Customize the layout
fig.update_layout(
    xaxis_title='Internet Usage Category',
    yaxis_title='Mean Score (Likert Scale: 1=Strongly Disagree, 5=Strongly Agree)',
    legend_title='Mental Health Factor',
    legend=dict(title='Mental Health Factor', x=1.05, y=1),
    margin=dict(l=60, r=100, t=80, b=60)
)

# Display Plotly chart in Streamlit
st.plotly_chart(fig, use_container_width=True)


