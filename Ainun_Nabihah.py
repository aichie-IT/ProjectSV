import streamlit as st
import pandas as pd
import plotly.express as px

st.subheader("🎯 Objective Statement")
st.write("""
The purpose of this visualization is to identify and analyze the demographic 
differences in mental health experiences among students, with a particular focus 
on how factors such as gender, age, race, and year of study influence students' 
perceptions and experiences of mental health challenges.
""")

st.title("Exploring Internet Use and Suicidality in Mental Health Populations")

# --- 1. DATA LOADING ---

@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQnrGG72xRS-qLoiM2zon4eP8t5XMiO5MhoLUEe2jJer0G5EzodiU4e0NOmx_ssmCwZf-AnbQXhBbTM/pub?gid=1791189796&single=true&output=csv"
    return pd.read_csv(url)

try:
    df = load_data()
    st.success("✅ Data loaded successfully from GitHub!")
    st.dataframe(df.head())
except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    st.stop()

# Use df directly 
filtered_data = df.copy()

# --- 2. DATA MAPPING ---
    
    # Mapping raw long column names to the short names used in your logic
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

df_original = load_data()
df = df_original.copy()

# --- 3. DATA TRANSFORMATION  ---

# Mapping Gender
gender_map = {0: 'Female', 1: 'Male', 2: 'Other'}
df['Gender_Num'] = df['Gender'].map({'Female': 0, 'Male': 1, 'Other': 2}).fillna(2)

# Mapping Year of Study
year_map = {1: 'Year 1', 2: 'Year 2', 3: 'Year 3', 4: 'Year 4', 5: 'Year 5', 0: 'Unknown'}
df['Year_of_Study_Num'] = df['Year_of_Study'].map({'Year 1': 1, 'Year 2': 2, 'Year 3': 3, 'Year 4': 4, 'Year 5': 5}).fillna(0)

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

# Mapping Impact
impact_map = {1: 'Positive Impact', 0: 'Negative Impact', 2: 'No impact'}
df['Social_Media_Positive_Impact_on_Wellbeing_Num'] = df['Social_Media_Positive_Impact_on_Wellbeing'].map({
    'Positive impact': 1, 'Negative impact': 0, 'No impact': 2
}).fillna(2)

# Mapping Race
race_map = {0: 'Malay', 1: 'Chinese', 2: 'Indian', 3: 'Other'}
df['Race_Num'] = df['Race'].map({'Malay': 0, 'Chinese': 1, 'Indian': 2, 'Others': 3, 'Other': 3}).fillna(3)

# --- 4. DATA FILTERING ---

# Filtered data subset
filtered_data = df[['Gender', 'Year_of_Study', 'Current_Living_Situation', 
                    'Social_Media_Positive_Impact_on_Wellbeing', 
                    'Difficulty_Sleeping_University_Pressure', 'Race', 
                    'Social_Media_Daily_Routine', 'Employment_Status']].dropna()


# --- 5. INDIVIDUAL VISUALIZATIONS ---

# Layout into two columns
col1, col2 = st.columns(2)

with col1:
    # VISUALIZATION 1 : Gender Distribution Across Year of Study
    st.subheader("Gender Distribution Across Year of Study")
    
    # METRIC 1: Total Count and Dominant Gender
    total_respondents = len(df)
    dominant_gender = df['Gender'].mode()[0]
    st.metric("Total Respondents", f"{total_respondents}", f"Majority: {dominant_gender}")
    
    fig1 = px.histogram(df, x='Year_of_Study', color='Gender', barmode='group',
                       category_orders={"Year_of_Study": ["Year 1", "Year 2", "Year 3", "Year 4", "Year 5"]},
                       color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown("""
**Interpretation:** The data shows that **Year 1 students** have the highest participation rate. 
The female students always have the majority over the male students in majority of the years.
""")


    # VISUALIZATION 2 : Gender vs. Social Media Impact
    
    # METRIC 2: Negative Impact Percentage
    neg_impact_count = len(df[df['Social_Media_Positive_Impact_on_Wellbeing'] == 'Negative impact'])
    neg_impact_pct = (neg_impact_count / total_respondents) * 100
    st.metric("Negative Impact Rate", f"{neg_impact_pct:.1f}%", "Impact on wellbeing")
    
    fig3 = px.histogram(df, x='Gender', color='Social_Media_Positive_Impact_on_Wellbeing', 
                       barmode='stack', 
                       color_discrete_map={'Positive impact': 'lightgreen', 'Negative impact': 'salmon', 'No impact': 'grey'})
    st.plotly_chart(fig3, use_container_width=True)
     st.markdown("""
**Interpretation:** The data show that the Year 1 students primarily live in the campus but Year 3 and Year 4 students are mainly off-campus.
This implies a change towards the independent living as students mature in their education.
""")

   
    # VISUALIZATION 3 : Gender vs. Difficulty Sleeping
    st.subheader("Gender vs. Difficulty Sleeping")
    
    # METRIC 3: High Difficulty Sleeping Count
    # Assuming "Strongly agree" and "Agree" are the high-stress indicators
    high_difficulty = filtered_data[filtered_data['Difficulty_Sleeping_University_Pressure'].isin(['Strongly agree', 'Agree'])]
    difficulty_pct = (len(high_difficulty) / len(filtered_data)) * 100
    st.metric("Sleep Difficulty Rate", f"{difficulty_pct:.1f}%", "Due to Uni pressure")
    
    fig5 = px.histogram(filtered_data, x='Difficulty_Sleeping_University_Pressure', color='Gender', 
                       barmode='group', color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown("""
**Interpretation:** The data display that the female students show more positive and negative effects of social media than the male students.
This implies that the overall impact of social media on the wellbeing of female students is more high.
""")


with col2:
    # VISUALIZATION 4 : Year of Study vs Current Living Situation
    st.subheader("Heatmap: Year vs Living Situation")
    
    # METRIC 4: Most Common Living Situation
    top_living = df['Current_Living_Situation'].mode()[0]
    st.metric("Primary Living Situation", top_living)
    
    year_living_xtab = pd.crosstab(df['Year_of_Study'], df['Current_Living_Situation'])
    fig2 = px.imshow(year_living_xtab, text_auto=True, color_continuous_scale='YlGnBu')
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("""
**Interpretation:** The data shows that Malay students also mention social media most commonly as a part of their day to day lives particularly at higher levels.
Some other racial groups demonstrate less and less consistent daily use of social media.
""")


    # VISUALIZATION 5 : Race vs. Social Media Routine
    st.subheader("Race vs. Social Media Routine")
    
    # METRIC 5: Daily Routine Integration
    # Calculating how many people say SM is an important part of their routine
    routine_important = filtered_data[filtered_data['Social_Media_Daily_Routine'].isin(['Strongly agree', 'Agree'])]
    routine_pct = (len(routine_important) / len(filtered_data)) * 100
    st.metric("High SM Integration", f"{routine_pct:.1f}%", "Part of daily routine")
    
    fig4 = px.histogram(filtered_data, x='Social_Media_Daily_Routine', color='Race', 
                       barmode='group', color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown("""
**Interpretation:** The data shows that Malay students also mention social media most commonly as a part of their day to day lives particularly at higher levels.
Some other racial groups demonstrate less and less consistent daily use of social media.
""")


    # VISUALIZATION 6 : Employment Status
    st.subheader("Employment Status Distribution")
    
    # METRIC 6: Full-time Student Percentage
    ft_student_count = len(df[df['Employment_Status'] == 'Full-time student'])
    ft_student_pct = (ft_student_count / total_respondents) * 100
    st.metric("Full-time Students", f"{ft_student_pct:.1f}%", "Of total population")
    
    fig6 = px.pie(df, names='Employment_Status', 
                 color_discrete_sequence=px.colors.qualitative.Pastel) 
    fig6.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig6, use_container_width=True)
    st.markdown("""
**Interpretation:** The data shows that most of the respondents were full-time students and smaller percentage of them were taken up with paid jobs or internships.
This shows that the majority of students are basically interested in their studies and less are doing academics and career related activities.
""")

#Summary text
st.markdown("""
**Summary:** The visualizations show clear demographic differences in student's mental health experiences. 
Female students report greater effects from academic pressure and social media while higher-year students like to live more independently off-campus.
Most respondents are full-time students, showing that academic demands are a key factor influencing student wellbeing.
""")
