import streamlit as st
import pandas as pd

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Scientific Visualization : Project Group",
    layout="wide"
)

st.header("Scientific Visualization : Project Group", divider="gray")

# ==================================================
# OBJECTIVE
# ==================================================
st.subheader("🎯 Objective Statement")
st.write("""
The purpose of this visualization is to identify and analyze demographic 
differences in mental health experiences among students, focusing on how 
gender, race, and year of study influence students’ perceptions and experiences.
""")

# ==================================================
# DATA LOADING AND MAPPING
# ==================================================
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQnrGG72xRS-qLoiM2zon4eP8t5XMiO5MhoLUEe2jJer0G5EzodiU4e0NOmx_ssmCwZf-AnbQXhBbTM/pub?gid=1791189796&single=true&output=csv"
    df = pd.read_csv(url)

    column_mapping = {
        'Gender / Jantina:': 'Gender',
        'Year of Study / Tahun Belajar:': 'Year_of_Study',
        'Current living situation / Keadaan hidup sekarang:': 'Current_Living_Situation',
        'Employment Status / Status Pekerjaan:': 'Employment_Status',
        'Race / Bangsa:': 'Race',
        'Social media has a generally positive impact on my wellbeing. / Media sosial secara amnya mempunyai kesan positif terhadap kesejahteraan saya.':
            'Social_Media_Positive_Impact_on_Wellbeing',
        'I have difficulty sleeping due to university-related pressure. / Saya sukar tidur kerana tekanan berkaitan universiti.':
            'Difficulty_Sleeping_University_Pressure',
        'Using social media is an important part of my daily routine. / Menggunakan media sosial adalah bahagian penting dalam rutin harian saya.':
            'Social_Media_Daily_Routine'
    }

    return df.rename(columns=column_mapping)

df = load_data()
st.success("✅ Data loaded successfully")
st.dataframe(df.head())

# ==================================================
# DATA TRANSFORMATION
# ==================================================
df['Gender_Num'] = df['Gender'].map({'Female': 0, 'Male': 1, 'Other': 2})
df['Year_Num'] = df['Year_of_Study'].str.extract(r'(\d)').astype(float)
df['Race_Num'] = df['Race'].map({
    'Malay': 0, 'Chinese': 1, 'Indian': 2, 'Other': 3, 'Others': 3
})

# ==================================================
# DATA FILTERING (SIDEBAR)
# ==================================================
st.sidebar.header("🔍 Data Filters")

gender_filter = st.sidebar.multiselect(
    "Gender",
    options=df['Gender'].dropna().unique(),
    default=df['Gender'].dropna().unique()
)

year_filter = st.sidebar.multiselect(
    "Year of Study",
    options=df['Year_of_Study'].dropna().unique(),
    default=df['Year_of_Study'].dropna().unique()
)

race_filter = st.sidebar.multiselect(
    "Race",
    options=df['Race'].dropna().unique(),
    default=df['Race'].dropna().unique()
)

filtered_data = df[
    (df['Gender'].isin(gender_filter)) &
    (df['Year_of_Study'].isin(year_filter)) &
    (df['Race'].isin(race_filter))
].dropna()

# ==================================================
# SUMMARY METRIC BOXES
# ==================================================
st.subheader("📊 Summary Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Respondents", len(filtered_data))

with col2:
    st.metric("Majority Gender", filtered_data['Gender'].mode()[0])

with col3:
    st.metric("Most Common Race", filtered_data['Race'].mode()[0])

with col4:
    st.metric("Dominant Year", filtered_data['Year_of_Study'].mode()[0])

# ==================================================
# SUMMARY
# ==================================================
st.markdown("""
### 📌 Summary

The analysis reveals clear demographic differences in students’ mental health experiences.  
Female students form the majority of respondents and demonstrate stronger perceived impacts 
from social media and academic pressure. Senior students are more likely to live independently, 
indicating a shift in lifestyle as academic progression increases.  

Overall, the findings suggest that **academic demands and social media usage are key factors 
influencing student wellbeing**, particularly among full-time and early-year students.
""")
