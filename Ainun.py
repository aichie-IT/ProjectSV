import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Demographic Analysis",
    layout="wide"
)

# ==================================================
# LOAD DATA
# ==================================================
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQnrGG72xRS-qLoiM2zon4eP8t5XMiO5MhoLUEe2jJer0G5EzodiU4e0NOmx_ssmCwZf-AnbQXhBbTM/pub?gid=1791189796&single=true&output=csv"
    return pd.read_csv(url)

df = load_data()
df.columns = df.columns.str.strip()

# ==================================================
# RENAME COLUMNS (REQUIRED ONLY)
# ==================================================
df = df.rename(columns={
    "Gender / Jantina:": "Gender",
    "Race / Bangsa:": "Race",
    "Year of Study / Tahun Belajar:": "Year_of_Study",
    "Current living situation / Keadaan hidup sekarang:": "Current_Living_Situation",
    "Employment Status / Status Pekerjaan:": "Employment_Status",
    "I have difficulty sleeping due to university-related pressure. / Saya sukar tidur kerana tekanan berkaitan universiti.": "Difficulty_Sleeping_University_Pressure",
    "Using social media is an important part of my daily routine. / Menggunakan media sosial adalah bahagian penting dalam rutin harian saya.": "Social_Media_Daily_Routine",
    "Social media has a generally positive impact on my wellbeing. / Media sosial secara amnya mempunyai kesan positif terhadap kesejahteraan saya.": "Social_Media_Positive_Impact_on_Wellbeing"
})

# ==================================================
# FIX ENCODING
# ==================================================
df = df.replace({"â\x80\x93": "-", "–": "-", "—": "-"}, regex=True)

# ==================================================
# LIKERT SCALE (1–5)
# ==================================================
likert_map = {
    "Strongly disagree": 1,
    "Disagree": 2,
    "Neutral": 3,
    "Agree": 4,
    "Strongly agree": 5
}

df["Difficulty_Sleeping_University_Pressure_Num"] = (
    df["Difficulty_Sleeping_University_Pressure"]
    .map(likert_map)
    .fillna(3)
)

df["Social_Media_Daily_Routine_Num"] = (
    df["Social_Media_Daily_Routine"]
    .map(likert_map)
    .fillna(3)
)

# ==================================================
# FILTER DATA
# ==================================================
filtered_data = df[
    [
        "Gender",
        "Year_of_Study",
        "Race",
        "Employment_Status",
        "Current_Living_Situation",
        "Difficulty_Sleeping_University_Pressure",
        "Social_Media_Daily_Routine",
        "Social_Media_Positive_Impact_on_Wellbeing"
    ]
].dropna()

# ==================================================
# TAB 4: DEMOGRAPHIC ANALYSIS
# ==================================================
st.title("Demographic Analysis of Student Mental Health")

st.write("""
This section explores demographic differences in students’ mental health experiences,
focusing on gender, race, year of study, living situation, and employment status.
""")

# ==================================================
# SUMMARY METRICS
# ==================================================
TOTAL_RESPONDENTS = len(df)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Respondents", TOTAL_RESPONDENTS)

with col2:
    st.metric(
        "Majority Gender",
        filtered_data["Gender"].mode()[0]
    )

with col3:
    st.metric(
        "Dominant Year of Study",
        filtered_data["Year_of_Study"].mode()[0]
    )

st.success("""
**Summary:**  
The survey consists of 101 respondents. Female students form the majority, and Year 4
students are the most represented group, suggesting that senior students experience
greater academic and mental health pressures.
""")

# ==================================================
# VISUALIZATIONS
# ==================================================
left, right = st.columns(2)

with left:
    st.subheader("Gender Distribution Across Year of Study")

    fig1 = px.histogram(
        filtered_data,
        x="Year_of_Study",
        color="Gender",
        barmode="group"
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Gender vs Difficulty Sleeping")

    fig2 = px.histogram(
        filtered_data,
        x="Difficulty_Sleeping_University_Pressure",
        color="Gender",
        barmode="group"
    )
    st.plotly_chart(fig2, use_container_width=True)

with right:
    st.subheader("Race vs Social Media Daily Routine")

    fig3 = px.histogram(
        filtered_data,
        x="Social_Media_Daily_Routine",
        color="Race",
        barmode="group"
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Employment Status Distribution")

    fig4 = px.pie(
        filtered_data,
        names="Employment_Status"
    )
    st.plotly_chart(fig4, use_container_width=True)

# ==================================================
# OBSERVATION
# ==================================================
st.success("""
**Observation:**  
Female students report higher levels of academic pressure and sleep difficulties.
Senior students tend to live more independently and integrate social media more into
their daily routines. Academic workload remains a key factor affecting student wellbeing.
""")
