import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Scientific Visualization : Project Group",
    layout="wide"
)

st.header("Scientific Visualization : Project Group", divider="gray")

st.subheader("🎯 Objective Statement")
st.write("""
The purpose of this visualization is to identify and analyze the demographic 
differences in mental health experiences among students, with a particular focus 
on how factors such as gender, age, race, and year of study influence students' 
perceptions and experiences of mental health challenges.
""")

st.title("Exploring Internet Use and Suicidality in Mental Health Populations")

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/s22a0050-ainun/SS2200/refs/heads/main/Exploring%20Internet%20Use%20and%20Suicidality%20in%20Mental%20Health%20Populations.csv"
    return pd.read_csv(url)

try:
    df = load_data()
    st.success("✅ Data loaded successfully from GitHub!")
    st.dataframe(df.head())
except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    st.stop()

# Use df directly (no undefined filtered_data)
filtered_data = df.copy()


# --- 4. INDIVIDUAL VISUALIZATIONS ( AINUN ) ---
# (Your existing columns and plotly charts follow here...)


st.title("📊 Individual Visualizations : Ainun")

import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. DATA LOADING ---

@st.cache_data
def load_data():
    # Load the uploaded CSV
    df = pd.read_csv('Exploring Internet Use and Suicidality in Mental Health Populations.csv')

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

# --- 5. INDIVIDUAL VISUALIZATIONS ( AINUN ) ---

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
Female students consistently outnumber male students across most years.
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


with col2:
    # VISUALIZATION 4 : Year of Study vs Current Living Situation
    st.subheader("Heatmap: Year vs Living Situation")
    
    # METRIC 4: Most Common Living Situation
    top_living = df['Current_Living_Situation'].mode()[0]
    st.metric("Primary Living Situation", top_living)
    
    year_living_xtab = pd.crosstab(df['Year_of_Study'], df['Current_Living_Situation'])
    fig2 = px.imshow(year_living_xtab, text_auto=True, color_continuous_scale='YlGnBu')
    st.plotly_chart(fig2, use_container_width=True)


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
