import streamlit as st
import pandas as pd
import plotly.express as px

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

st.title("Exploring Internet Use and Suicidality in Mental Health Populations")

# ==================================================
# DATA LOADING & COLUMN MAPPING
# ==================================================
@st.cache_data
def load_data():
    df = pd.read_csv(
        "Exploring Internet Use and Suicidality in Mental Health Populations.csv"
    )

    column_mapping = {
        "Gender / Jantina:": "Gender",
        "Year of Study / Tahun Belajar:": "Year_of_Study",
        "Race / Bangsa:": "Race",
        "Employment Status / Status Pekerjaan:": "Employment_Status",
        "Current living situation / Keadaan hidup sekarang:": "Current_Living_Situation",
        "Social media has a generally positive impact on my wellbeing. / Media sosial secara amnya mempunyai kesan positif terhadap kesejahteraan saya.":
            "Social_Media_Positive_Impact_on_Wellbeing",
        "I have difficulty sleeping due to university-related pressure. / Saya sukar tidur kerana tekanan berkaitan universiti.":
            "Difficulty_Sleeping_University_Pressure",
        "Using social media is an important part of my daily routine. / Menggunakan media sosial adalah bahagian penting dalam rutin harian saya.":
            "Social_Media_Daily_Routine"
    }

    return df.rename(columns=column_mapping)

df = load_data()
st.success("✅ Data loaded successfully")

# ==================================================
# TOTAL RESPONDENTS (RAW DATA)
# ==================================================
TOTAL_RESPONDENTS = len(df)

# ==================================================
# DATA TRANSFORMATION
# ==================================================
df["Year_Num"] = df["Year_of_Study"].str.extract(r"(\d)").astype(float)

# ==================================================
# DATA FILTERING (USER CONTROLLED)
# ==================================================
st.sidebar.header("🔍 Data Filtering")

gender_filter = st.sidebar.multiselect(
    "Gender",
    df["Gender"].dropna().unique(),
    df["Gender"].dropna().unique()
)

year_filter = st.sidebar.multiselect(
    "Year of Study",
    df["Year_of_Study"].dropna().unique(),
    df["Year_of_Study"].dropna().unique()
)

race_filter = st.sidebar.multiselect(
    "Race",
    df["Race"].dropna().unique(),
    df["Race"].dropna().unique()
)

filtered_data = df[
    (df["Gender"].isin(gender_filter)) &
    (df["Year_of_Study"].isin(year_filter)) &
    (df["Race"].isin(race_filter))
]

# ==================================================
# SUMMARY METRIC BOXES
# ==================================================
st.subheader("📊 Summary Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Respondents", TOTAL_RESPONDENTS)

with col2:
    st.metric("Filtered Respondents", len(filtered_data))

with col3:
    majority_gender = filtered_data["Gender"].mode(dropna=True)[0] if not filtered_data.empty else "N/A"
    st.metric("Majority Gender", majority_gender)

with col4:
    dominant_year = filtered_data["Year_of_Study"].mode(dropna=True)[0] if not filtered_data.empty else "N/A"
    st.metric("Dominant Year", dominant_year)

# ==================================================
# VISUALIZATIONS WITH INTERPRETATION
# ==================================================
left, right = st.columns(2)

with left:
    st.subheader("1️⃣ Gender Distribution Across Year of Study")

    fig1 = px.histogram(
        filtered_data,
        x="Year_of_Study",
        color="Gender",
        barmode="group",
        labels={"Year_of_Study":"Year of Study","count":"Number of Students"}
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("""
    **Interpretation:**  
   The data shows that students in Year 1 are the most active. The female students always have the majority over the male students in majority of the years.
    """)

    st.subheader("2️⃣ Gender vs Social Media Impact")

    fig2 = px.histogram(
        filtered_data,
        x="Gender",
        color="Social_Media_Positive_Impact_on_Wellbeing",
        barmode="stack",
        labels={"Social_Media_Positive_Impact_on_Wellbeing":"Perceived Positive Impact","count":"Number of Students"}
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    **Interpretation:**  
   The data shows that the Year 1 students primarily stay in the campus but Year 3 and Year 4 students are mainly off-campus.
   This implies a change towards the independent living as students mature in their education.

    """)

    st.subheader("3️⃣ Gender vs Difficulty Sleeping")

    fig3 = px.histogram(
        filtered_data,
        x="Difficulty_Sleeping_University_Pressure",
        color="Gender",
        barmode="group",
        labels={"Difficulty_Sleeping_University_Pressure":"Difficulty Sleeping","count":"Number of Students"}
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("""
    **Interpretation:**  
    Female students report slightly higher difficulty sleeping due to university-related 
    pressure. Sleep disturbances may be linked to academic stress and social factors.
    """)

with right:
    st.subheader("4️⃣ Year of Study vs Living Situation")

    heatmap_data = pd.crosstab(
        filtered_data["Year_of_Study"],
        filtered_data["Current_Living_Situation"]
    )

    fig4 = px.imshow(
        heatmap_data,
        text_auto=True,
        color_continuous_scale="YlGnBu",
        labels={"x":"Living Situation","y":"Year of Study","color":"Count"}
    )
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("""
    **Interpretation:**  
    The data shows that Malay students also mention social media most commonly as a part of their day to lives particularly at higher levels of agreement.
    Some other racial groups demonstrate less and less consistent daily use of social media.
    """)

    st.subheader("5️⃣ Race vs Social Media Routine")

    fig5 = px.histogram(
        filtered_data,
        x="Social_Media_Daily_Routine",
        color="Race",
        barmode="group",
        labels={"Social_Media_Daily_Routine":"Social Media Routine","count":"Number of Students"}
    )
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("""
    **Interpretation:**  
    Usage of social media as part of the daily routine varies slightly across races, 
    suggesting that cultural or social normal may influence online engagement.
    """)

    st.subheader("6️⃣ Employment Status Distribution")

    fig6 = px.pie(
        filtered_data,
        names="Employment_Status",
        labels={"Employment_Status":"Employment Status"}
    )
    st.plotly_chart(fig6, use_container_width=True)

    st.markdown("""
    **Interpretation:**  
    Most respondents are full-time students. Part-time employment is less common, 
    showing that academic commitments influence daily routines.
    """)

# ==================================================
# SUMMARY
# ==================================================
st.markdown("""
### 📌 Summary

The visualizations show clear demographic differences in student's mental health experiences. Female students report greater 
effects from academic pressure and social media while higher-year students like to live more independently off-campus.
Most respondents are full-time students, showing that academic demands are a key factor influencing student wellbeing.
""")
