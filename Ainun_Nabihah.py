import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE HEADER
# =========================
st.title("Exploring Demographic Differences in Student Mental Health")

st.subheader("🎯 Objective Statement")
st.write("""
The purpose of this visualization is to identify and analyze demographic 
differences in mental health experiences among students, focusing on factors 
such as gender, race, year of study, living situation, employment status, and 
social media usage.
""")

# =========================
# DATA LOADING & CLEANING
# =========================
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQnrGG72xRS-qLoiM2zon4eP8t5XMiO5MhoLUEe2jJer0G5EzodiU4e0NOmx_ssmCwZf-AnbQXhBbTM/pub?gid=1791189796&single=true&output=csv"
    df = pd.read_csv(url)

    # Rename long columns
    column_mapping = {
        'Gender / Jantina:': 'Gender',
        'Year of Study / Tahun Belajar:': 'Year_of_Study',
        'Current living situation / Keadaan hidup sekarang:': 'Current_Living_Situation',
        'Employment Status / Status Pekerjaan:': 'Employment_Status',
        'Race / Bangsa:': 'Race',
        'Social media has a generally positive impact on my wellbeing. / Media sosial secara amnya mempunyai kesan positif terhadap kesejahteraan saya.': 'Social_Media_Positive_Impact_on_Wellbeing',
        'I have difficulty sleeping due to university-related pressure. / Saya sukar tidur kerana tekanan berkaitan universiti.': 'Difficulty_Sleeping_University_Pressure',
        'Using social media is an important part of my daily routine. / Menggunakan media sosial adalah bahagian penting dalam rutin harian saya.': 'Social_Media_Daily_Routine'
    }

    df = df.rename(columns=column_mapping)
    return df


df = load_data()
st.success("✅ Data loaded successfully")
st.dataframe(df.head())

# Remove missing values for analysis
filtered_data = df.dropna()

total_respondents = len(filtered_data)

# =========================
# VISUALIZATIONS
# =========================
col1, col2 = st.columns(2)

# -------- COLUMN 1 --------
with col1:

    # VISUALIZATION 1
    st.subheader("Gender Distribution Across Year of Study")

    dominant_gender = filtered_data['Gender'].mode()[0]
    st.metric("Total Respondents", total_respondents, f"Majority: {dominant_gender}")

    fig1 = px.histogram(
        filtered_data,
        x="Year_of_Study",
        color="Gender",
        barmode="group",
        category_orders={"Year_of_Study": ["Year 1", "Year 2", "Year 3", "Year 4", "Year 5"]},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("""
**Interpretation:** Female students dominate across most years of study, particularly in the early academic years.
This suggests a higher participation rate of female students in the survey sample.
""")

    # VISUALIZATION 2
    st.subheader("Gender vs Social Media Impact on Wellbeing")

    neg_impact_pct = (
        len(filtered_data[filtered_data['Social_Media_Positive_Impact_on_Wellbeing'] == 'Negative impact'])
        / total_respondents
    ) * 100

    st.metric("Negative Impact Rate", f"{neg_impact_pct:.1f}%")

    fig2 = px.histogram(
        filtered_data,
        x="Gender",
        color="Social_Media_Positive_Impact_on_Wellbeing",
        barmode="stack"
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
**Interpretation:** Female students report a higher overall impact of social media, including both positive and negative effects,
indicating greater sensitivity to social media influence on wellbeing.
""")

    # VISUALIZATION 3
    st.subheader("Gender vs Difficulty Sleeping")

    high_sleep_diff = filtered_data[
        filtered_data['Difficulty_Sleeping_University_Pressure'].isin(['Agree', 'Strongly agree'])
    ]
    sleep_pct = (len(high_sleep_diff) / total_respondents) * 100

    st.metric("Sleep Difficulty Rate", f"{sleep_pct:.1f}%")

    fig3 = px.histogram(
        filtered_data,
        x="Difficulty_Sleeping_University_Pressure",
        color="Gender",
        barmode="group"
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("""
**Interpretation:** Female students experience higher levels of sleep difficulty due to university-related pressure,
suggesting stronger academic stress among female respondents.
""")

# -------- COLUMN 2 --------
with col2:

    # VISUALIZATION 4
    st.subheader("Year of Study vs Living Situation")

    top_living = filtered_data['Current_Living_Situation'].mode()[0]
    st.metric("Most Common Living Situation", top_living)

    living_table = pd.crosstab(
        filtered_data['Year_of_Study'],
        filtered_data['Current_Living_Situation']
    )

    fig4 = px.imshow(
        living_table,
        text_auto=True,
        color_continuous_scale="YlGnBu"
    )
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("""
**Interpretation:** Lower-year students tend to live on campus, while higher-year students increasingly live off-campus,
indicating growing independence as students progress academically.
""")

    # VISUALIZATION 5
    st.subheader("Race vs Social Media Daily Routine")

    routine_pct = (
        len(filtered_data[
            filtered_data['Social_Media_Daily_Routine'].isin(['Agree', 'Strongly agree'])
        ]) / total_respondents
    ) * 100

    st.metric("High Social Media Integration", f"{routine_pct:.1f}%")

    fig5 = px.histogram(
        filtered_data,
        x="Social_Media_Daily_Routine",
        color="Race",
        barmode="group"
    )
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("""
**Interpretation:** Malay students report higher daily social media usage compared to other racial groups,
suggesting cultural differences in digital engagement patterns.
""")

    # VISUALIZATION 6
    st.subheader("Employment Status Distribution")

    ft_pct = (
        len(filtered_data[filtered_data['Employment_Status'] == 'Full-time student'])
        / total_respondents
    ) * 100

    st.metric("Full-time Students", f"{ft_pct:.1f}%")

    fig6 = px.pie(
        filtered_data,
        names="Employment_Status"
    )
    st.plotly_chart(fig6, use_container_width=True)

    st.markdown("""
**Interpretation:** The majority of respondents are full-time students, indicating that academic responsibilities
are the primary focus and a major contributor to student stress levels.
""")

# =========================
# SUMMARY
# =========================
st.markdown("""
### 📌 Overall Summary

The visualizations reveal clear demographic differences in **students' mental health experiences**.
Female students consistently report greater academic pressure, sleep difficulties, and stronger social media impacts.
As students advance in their studies, they demonstrate increased independence through off-campus living.
Overall, the dominance of full-time students highlights academic demands as a key factor influencing student wellbeing.
""")
