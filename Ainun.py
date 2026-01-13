import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Demographic Difference with Mental Health Experiences",
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
# RENAME COLUMNS 
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

# --- DATA TRANSFORMATION FOR VISUALIZATIONS ---

# Mapping Gender
gender_map = {0: 'Female', 1: 'Male', 2: 'Other'}
df['Gender_Num'] = df['Gender'].map({'Female': 0, 'Male': 1, 'Other': 2}).fillna(2)

# Mapping Year of Study
year_map = {1: 'Year 1', 2: 'Year 2', 3: 'Year 3', 4: 'Year 4', 5: 'Year 5', 0: 'Unknown'}
df['Year_of_Study_Num'] = df['Year_of_Study'].map({'Year 1': 1, 'Year 2': 2, 'Year 3': 3, 'Year 4': 4, 'postgraduate': 5}).fillna(0)

# Mapping Living Situation
living_map = {0: 'With family', 1: 'On-campus', 2: 'Off-campus', 3: 'Other'}
df['Current_Living_Situation_Num'] = df['Current_Living_Situation'].map({
    'With family': 0, 'On-campus': 1, 'Off-campus (rental)': 2, 'Off-campus': 2, 'Other': 3
}).fillna(3)

# Mapping Employment (Clean string variations from CSV)
df['Employment_Status_Num'] = df['Employment_Status'].map({
    'Full-time student': 3,
    'In paid employment (including part-time, self-employed)': 2,
    'Internship': 1,
    'Unemployed': 0
}).fillna(2)

# Mapping Social Media Impact
impact_map = {1: 'Positive Impact', 0: 'Negative Impact', 2: 'No impact'}
df['Social_Media_Positive_Impact_on_Wellbeing_Num'] = df['Social_Media_Positive_Impact_on_Wellbeing'].map({
    'Positive impact': 1, 'Negative impact': 0, 'No impact': 2
}).fillna(2)

# Mapping Race
race_map = {0: 'Malay', 1: 'Chinese', 2: 'Indian', 3: 'Other'}
df['Race_Num'] = df['Race'].map({'Malay': 0, 'Chinese': 1, 'Indian': 2, 'Others': 3, 'Other': 4}).fillna(3)

# --- NEW: Mapping Difficulty Sleeping Due to University Pressure to 5-point Likert ---
sleep_map = {
    'Strongly disagree': 1,
    'Disagree': 2,
    'Neutral': 3,
    'Agree': 4,
    'Strongly agree': 5
}
df['Difficulty_Sleeping_University_Pressure_Num'] = df['Difficulty_Sleeping_University_Pressure'].map(sleep_map).fillna(3)

# --- NEW: Mapping Social Media Daily Routine to 5-point Likert ---
routine_map = {
    'Strongly disagree': 1,
    'Disagree': 2,
    'Neutral': 3,
    'Agree': 4,
    'Strongly agree': 5
}
df['Social_Media_Daily_Routine_Num'] = df['Social_Media_Daily_Routine'].map(routine_map).fillna(3)


# ==================================================
# TAB 4: DEMOGRAPHIC DIFFERENCES WITH MENTAL HEALTH EXPERIENCES
# ==================================================

st.title("Demographic Differences with Mental Health Experiences")

st.write("""
The purpose of this visualization is to identify and analyze demographic 
differences in mental health experiences among students, focusing on how 
gender, race and year of study influence student's perceptions and experience challenges.
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
The dataset is composed of 101 participants, which is an sample to see the significant trends in the mental health 
of students and their internet use. The survey is dominated by female who form majority of the respondents meaning that the female 
students are more represented in the survey. Regarding the level of study, Year 4 students are the majority group which implies that 
final-year students are the most represented and can have different academic and mental health issues as compared to the lower years.
""")
# ==================================================
# VISUALIZATIONS
# ==================================================

left, right = st.columns(2)

with left:
    ("1️⃣ Gender Distribution Across Year of Study")

    fig1 = px.histogram(
        filtered_data,
        x="Year_of_Study",
        color="Gender",
        barmode="group",
        labels={"Year_of_Study":"Year of Study","count":"Number of Respondents"}
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    st.success("""
        **Interpretation:** 
   The data shows that students in Year 1 are the most active. The female students always have the majority over the male students in majority of the years.
    """)

    ("2️⃣ Gender vs Social Media Impact")

    fig2 = px.histogram(
        filtered_data,
        x="Gender",
        color="Social_Media_Positive_Impact_on_Wellbeing",
        barmode="stack",
        labels={"Social_Media_Positive_Impact_on_Wellbeing":"Perceived Positive Impact","count":"Number of Respondents"}
    )
    st.plotly_chart(fig2, use_container_width=True)
     
    st.success("""
        **Interpretation:**  
   The data shows that the Year 1 students primarily stay in the campus but Year 3 and Year 4 students are mainly off-campus.
   This implies a change towards the independent living as students mature in their education.

    """)

    ("3️⃣ Gender vs Difficulty Sleeping")

    fig3 = px.histogram(
        filtered_data,
        x="Difficulty_Sleeping_University_Pressure",
        color="Gender",
        barmode="group",
        labels={"Difficulty_Sleeping_University_Pressure":"Difficulty Sleeping","count":"Number of Respondents"}
    )
    st.plotly_chart(fig3, use_container_width=True)
    
    st.success("""
        **Interpretation:**  
    Female students report slightly higher difficulty sleeping due to university-related 
    pressure. Sleep disturbances may be linked to academic stress and social factors.
    """)

with right:
    ("4️⃣ Year of Study vs Living Situation")

    heatmap_data = pd.crosstab(
        filtered_data["Year_of_Study"],
        filtered_data["Current_Living_Situation"]
    )

    fig4 = px.imshow(
        heatmap_data,
        text_auto=True,
        color_continuous_scale="YlGnBu",
        labels={"x":"Living Situation","y":"Year of Study","color":"count"}
    )
    st.plotly_chart(fig4, use_container_width=True)
     
    st.success("""
        **Interpretation:**  
    The data shows that Malay students also mention social media most commonly as a part of their day to lives particularly at higher levels of agreement.
    Some other racial groups demonstrate less and less consistent daily use of social media.
    """)

    ("5️⃣ Race vs Social Media Routine")

    fig5 = px.histogram(
        filtered_data,
        x="Social_Media_Daily_Routine",
        color="Race",
        barmode="group",
        labels={"Social_Media_Daily_Routine":"Social Media Routine","count":"Number of Respondents"}
    )
    st.plotly_chart(fig5, use_container_width=True)
    
    st.success("""
        **Interpretation:**  
    Usage of social media as part of the daily routine varies slightly across races, 
    suggesting that cultural or social normal may influence online engagement.
    """)

    ("6️⃣ Employment Status Distribution")

    fig6 = px.pie(
        filtered_data,
        names="Employment_Status",
        labels={"Employment_Status":"Employment Status"}
    )
    st.plotly_chart(fig6, use_container_width=True)
    
    st.success("""
        **Interpretation:** 
    Most respondents are full-time students. Part-time employment is less common, 
    showing that academic commitments influence daily routines.
    """)

# ==================================================
# OBSERVATION
# ==================================================

st.success("""
    **Observation:** 

The visualizations show clear demographic differences in student's mental health experiences. Female students report greater 
effects from academic pressure and social media while higher-year students like to live more independently off-campus.
Most respondents are full-time students, showing that academic demands are a key factor influencing student wellbeing.
""")
