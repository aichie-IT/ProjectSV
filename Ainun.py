import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================
# PAGE CONFIG (MUST BE FIRST)
# ==================================================
st.set_page_config(
    page_title="Scientific Visualization : Project Group",
    layout="wide"
)

# ==================================================
# DATA LOADING
# ==================================================
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQnrGG72xRS-qLoiM2zon4eP8t5XMiO5MhoLUEe2jJer0G5EzodiU4e0NOmx_ssmCwZf-AnbQXhBbTM/pub?gid=1791189796&single=true&output=csv"
    df = pd.read_csv(url)

    column_mapping = {
        "Gender / Jantina:": "Gender",
        "Year of Study / Tahun Belajar:": "Year_of_Study",
        "Race / Bangsa:": "Race",
        "Employment Status / Status Pekerjaan:": "Employment_Status",
        "Current living situation / Keadaan hidup sekarang:": "Current_Living_Situation",
        "Social media has a generally positive impact on my wellbeing. / Media sosial secara amnya mempunyai kesan positif terhadap kesejahteraan saya.": "Social_Media_Positive_Impact_on_Wellbeing",
        "I have difficulty sleeping due to university-related pressure. / Saya sukar tidur kerana tekanan berkaitan universiti.": "Difficulty_Sleeping_University_Pressure",
        "Using social media is an important part of my daily routine. / Menggunakan media sosial adalah bahagian penting dalam rutin harian saya.": "Social_Media_Daily_Routine"
    }

    return df.rename(columns=column_mapping)

df = load_data()

# ==================================================
# HEADER
# ==================================================
st.header("Scientific Visualization : Project Group", divider="gray")

st.subheader("🎯 Objective Statement")
st.write("""
The purpose of this visualization is to analyze demographic differences 
in mental health experiences among students.
""")

st.title("Exploring Internet Use and Suicidality in Mental Health Populations")

# ==================================================
# SIDEBAR FILTERS (SAFE)
# ==================================================
st.sidebar.header("🔍 Data Filtering")

gender_filter = st.sidebar.multiselect(
    "Gender",
    options=sorted(df["Gender"].dropna().unique()),
    default=df["Gender"].dropna().unique()
)

year_filter = st.sidebar.multiselect(
    "Year of Study",
    options=sorted(df["Year_of_Study"].dropna().unique()),
    default=df["Year_of_Study"].dropna().unique()
)

race_filter = st.sidebar.multiselect(
    "Race",
    options=sorted(df["Race"].dropna().unique()),
    default=df["Race"].dropna().unique()
)

filtered_data = df[
    (df["Gender"].isin(gender_filter)) &
    (df["Year_of_Study"].isin(year_filter)) &
    (df["Race"].isin(race_filter))
]

# ==================================================
# EMPTY DATA PROTECTION 🚨
# ==================================================
if filtered_data.empty:
    st.error("⚠️ No data available for the selected filters.")
    st.stop()

# ==================================================
# METRICS
# ==================================================
st.subheader("📊 Summary Metrics")

col1, col2 = st.columns(2)
col1.metric("Total Respondents", len(df))
col2.metric("Filtered Respondents", len(filtered_data))

# ==================================================
# VISUALIZATIONS
# ==================================================
st.subheader("📈 Distribution of Numeric Variables")

fig1 = px.histogram(
    filtered_data,
    x="Year_of_Study",
    color="Gender",
    barmode="group"
)
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.histogram(
    filtered_data,
    x="Gender",
    color="Social_Media_Positive_Impact_on_Wellbeing",
    barmode="stack"
)
st.plotly_chart(fig2, use_container_width=True)
