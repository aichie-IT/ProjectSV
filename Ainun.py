import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Scientific Visualization : Project Group",
    layout="wide"
)

st.header("Scientific Visualization : Project Group", divider="gray")

# --------------------------------------------------
# OBJECTIVE
# --------------------------------------------------
st.subheader("🎯 Objective Statement")
st.write("""
The purpose of this visualization is to identify and analyze the demographic 
differences in mental health experiences among students, with a particular focus 
on how factors such as gender, race, and year of study influence students' 
perceptions and experiences of mental health challenges.
""")

st.title("Exploring Internet Use and Suicidality in Mental Health Populations")

# --------------------------------------------------
# DATA LOADING
# --------------------------------------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/s22a0050-ainun/SS2200/main/Exploring%20Internet%20Use%20and%20Suicidality%20in%20Mental%20Health%20Populations.csv"
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

    df = df.rename(columns=column_mapping)
    return df

try:
    df = load_data()
    st.success("✅ Data loaded successfully!")
    st.dataframe(df.head())
except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    st.stop()

filtered_data = df.dropna()

st.markdown("""
**Summary:** The visualizations reveal clear demographic differences in students’ mental health experiences.  
Female students report stronger effects from social media and academic pressure, while senior students 
tend to live more independently off-campus. Most respondents are full-time students, highlighting 
academic demands as a major factor influencing student wellbeing.
""")

st.title("📊 Individual Visualizations : Ainun")

# --------------------------------------------------
# LAYOUT
# --------------------------------------------------
col1, col2 = st.columns(2)

# ==================================================
# COLUMN 1
# ==================================================
with col1:

    # --- VIS 1 ---
    st.subheader("Gender Distribution Across Year of Study")

    total_respondents = len(df)
    dominant_gender = df['Gender'].mode()[0]

    st.metric("Total Respondents", total_respondents, f"Majority: {dominant_gender}")

    fig1 = px.histogram(
        df,
        x="Year_of_Study",
        color="Gender",
        barmode="group",
        category_orders={"Year_of_Study": ["Year 1", "Year 2", "Year 3", "Year 4", "Year 5"]},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("""
**Interpretation:** Year 1 students form the largest group of respondents. 
Across almost all years, female students consistently outnumber male students.
""")

    # --- VIS 2 ---
    st.subheader("Gender vs Social Media Impact on Wellbeing")

    neg_pct = (
        df['Social_Media_Positive_Impact_on_Wellbeing']
        .eq('Negative impact')
        .mean() * 100
    )

    st.metric("Negative Impact Rate", f"{neg_pct:.1f}%")

    fig2 = px.histogram(
        df,
        x="Gender",
        color="Social_Media_Positive_Impact_on_Wellbeing",
        barmode="stack"
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
**Interpretation:** Female students report stronger positive and negative impacts 
of social media compared to male students, suggesting higher emotional engagement.
""")

    # --- VIS 3 ---
    st.subheader("Gender vs Difficulty Sleeping")

    high_sleep = filtered_data[
        filtered_data['Difficulty_Sleeping_University_Pressure'].isin(['Agree', 'Strongly agree'])
    ]

    sleep_pct = len(high_sleep) / len(filtered_data) * 100
    st.metric("Sleep Difficulty Rate", f"{sleep_pct:.1f}%")

    fig3 = px.histogram(
        filtered_data,
        x="Difficulty_Sleeping_University_Pressure",
        color="Gender",
        barmode="group"
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("""
**Interpretation:** Female students show higher agreement levels regarding 
sleep difficulties caused by university-related pressure.
""")

# ==================================================
# COLUMN 2
# ==================================================
with col2:

    # --- VIS 4 ---
    st.subheader("Year of Study vs Living Situation")

    top_living = df['Current_Living_Situation'].mode()[0]
    st.metric("Most Common Living Situation", top_living)

    ctab = pd.crosstab(df['Year_of_Study'], df['Current_Living_Situation'])
    fig4 = px.imshow(ctab, text_auto=True, color_continuous_scale="YlGnBu")
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("""
**Interpretation:** Junior students mostly live on-campus, while senior students 
tend to move off-campus, reflecting increasing independence.
""")

    # --- VIS 5 ---
    st.subheader("Race vs Social Media Daily Routine")

    routine_pct = (
        filtered_data['Social_Media_Daily_Routine']
        .isin(['Agree', 'Strongly agree'])
        .mean() * 100
    )

    st.metric("High Social Media Integration", f"{routine_pct:.1f}%")

    fig5 = px.histogram(
        filtered_data,
        x="Social_Media_Daily_Routine",
        color="Race",
        barmode="group"
    )
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("""
**Interpretation:** Malay students show the strongest daily social media usage, 
while other racial groups demonstrate more varied usage patterns.
""")

    # --- VIS 6 ---
    st.subheader("Employment Status Distribution")

    ft_pct = (df['Employment_Status'] == 'Full-time student').mean() * 100
    st.metric("Full-time Students", f"{ft_pct:.1f}%")

    fig6 = px.pie(
        df,
        names="Employment_Status",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig6.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig6, use_container_width=True)

    st.markdown("""
**Interpretation:** Most respondents are full-time students, indicating that 
academic responsibilities are the dominant focus of the population.
""")

