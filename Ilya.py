import pandas as pd
import plotly.express as px
import streamlit as st

# --- LOAD DATA ---
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQnrGG72xRS-qLoiM2zon4eP8t5XMiO5MhoLUEe2jJer0G5EzodiU4e0NOmx_ssmCwZf-AnbQXhBbTM/pub?gid=1791189796&single=true&output=csv"
    return pd.read_csv(url)

df = load_data()

st.title("Relationship Between Internet Usage and Mental Health Outcomes")

# Display a brief explanation of the project
st.write("""Analyzing how different patterns of internet use,
such as daily usage duration, frequency, and usage before sleep, are associated with indicators of 
mental health, including stress, anxiety, and depression, among UMK students. 
""")

# --- Grouped Bar Chart ---
st.subheader("Average Mental Health Scores by Internet Usage Level")
fig, ax = plt.subplots(figsize=(12, 7))

sns.barplot(
    x='Internet_Usage_Category',
    y='Score',
    hue='Mental_Health_Factor',
    data=df_melted,
    errorbar=None,  # Display mean
    order=['Low', 'Moderate', 'High'],
    ax=ax
)

ax.set_title('Average Mental Health Scores by Internet Usage Level')
ax.set_xlabel('Internet Usage Category')
ax.set_ylabel('Mean Score (Likert Scale: 1=Strongly Disagree, 5=Strongly Agree)')
ax.legend(title='Mental Health Factor', bbox_to_anchor=(1.05, 1), loc='upper left')

# Display the plot
st.pyplot(fig)

# Create the box plot
st.subheader("Difficulty Sleeping Due to University Pressure by Social Media Affecting Sleep")

fig, ax = plt.subplots(figsize=(8, 6))

sns.boxplot(
    x='Internet_Use_Affects_Sleep',
    y='Difficulty_Sleeping_University_Pressure_Score',
    data=df_plot,
    palette='magma',
    order=['No', 'Yes'],  # Ensure 'No' comes before 'Yes' on the x-axis
    ax=ax
)

ax.set_title('Difficulty Sleeping Due to University Pressure by Social Media Affecting Sleep')
ax.set_xlabel('Social Media Affects Sleep (Yes/No)')
ax.set_ylabel('Difficulty Sleeping Score (1=Strongly Disagree, 5=Strongly Agree)')
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Display the plot
st.pyplot(fig)

