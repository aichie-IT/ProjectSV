import streamlit as st
import pandas as pd
import plotly.express as px

# --- LOAD DATA ---
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQnrGG72xRS-qLoiM2zon4eP8t5XMiO5MhoLUEe2jJer0G5EzodiU4e0NOmx_ssmCwZf-AnbQXhBbTM/pub?gid=1791189796&single=true&output=csv"
    return pd.read_csv(url)

df = load_data()

# Clean column names
df.columns = df.columns.str.strip()

# Rename columns (unchanged from your code)
df = df.rename(columns={
    "How often do you use social media? / Berapa kerap anda menggunakan media sosial?": "Social_Media_Use_Frequency",
    "I have been feeling stressed or overwhelmed with assignments. / Saya telah berasa tertekan atau terbeban dengan tugasan.": "Assignments_Stress",
    "I often feel anxious about my academic workload. / Saya sering berasa bimbang tentang beban kerja akademik saya.": "Academic_Workload_Anxiety",
    "I have difficulty sleeping due to university-related pressure. / Saya sukar tidur kerana tekanan berkaitan universiti.": "Difficulty_Sleeping_University_Pressure",
    "Social media has a generally negative impact on my wellbeing. / Media sosial secara amnya mempunyai kesan negatif terhadap kesejahteraan saya.": "Social_Media_Negative_Impact_on_Wellbeing",
    "Platforms you use most often (select all) / Platform yang paling kerap anda gunakan (pilih semua):": "Platforms_Most_Often_Used"
})

# --- MAP SOCIAL MEDIA FREQUENCY ---
short_label_map = {
    "Less than 1 hour per day": "< 1 hr",
    "1 to 2 hours per day": "1–2 hrs",
    "3 to 4 hours per day": "3–4 hrs",
    "5 to 6 hours per day": "5–6 hrs",
    "More than 6 hours per day": "> 6 hrs"
}

df["Social_Media_Use_Frequency"] = df["Social_Media_Use_Frequency"].map(short_label_map)

# --- INTERNET USAGE CATEGORY ---
internet_usage_categories = {
    "< 1 hr": "Low",
    "1–2 hrs": "Low",
    "3–4 hrs": "Moderate",
    "5–6 hrs": "High",
    "> 6 hrs": "High"
}

df["Internet_Usage_Category"] = df["Social_Media_Use_Frequency"].map(
    internet_usage_categories
)

# --- MENTAL HEALTH COLUMNS ---
mental_health_cols = [
    "Assignments_Stress",
    "Academic_Workload_Anxiety",
    "Difficulty_Sleeping_University_Pressure",
    "Social_Media_Negative_Impact_on_Wellbeing"
]

# Convert to numeric
for col in mental_health_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# --- MELT DATA ---
df_melted = df.melt(
    id_vars="Internet_Usage_Category",
    value_vars=mental_health_cols,
    var_name="Mental_Health_Factor",
    value_name="Score"
)

# Rename factors for readability
mental_health_factor_map = {
    "Assignments_Stress": "Stress from Assignments",
    "Academic_Workload_Anxiety": "Academic Workload Anxiety",
    "Difficulty_Sleeping_University_Pressure": "Difficulty Sleeping (Pressure)",
    "Social_Media_Negative_Impact_on_Wellbeing": "Negative Social Media Impact"
}

df_melted["Mental_Health_Factor"] = df_melted["Mental_Health_Factor"].map(
    mental_health_factor_map
)

# Category order
order = ["Low", "Moderate", "High"]
df_melted["Internet_Usage_Category"] = pd.Categorical(
    df_melted["Internet_Usage_Category"],
    categories=order,
    ordered=True
)

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

