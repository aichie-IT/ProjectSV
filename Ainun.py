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

# --- DATA TRANSFORMATION FOR VISUALIZATIONS ---

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

# Mapping Social Media Impact
impact_map = {1: 'Positive Impact', 0: 'Negative Impact', 2: 'No impact'}
df['Social_Media_Positive_Impact_on_Wellbeing_Num'] = df['Social_Media_Positive_Impact_on_Wellbeing'].map({
    'Positive impact': 1, 'Negative impact': 0, 'No impact': 2
}).fillna(2)

# Mapping Race
race_map = {0: 'Malay', 1: 'Chinese', 2: 'Indian', 3: 'Other'}
df['Race_Num'] = df['Race'].map({'Malay': 0, 'Chinese': 1, 'Indian': 2, 'Others': 3, 'Other': 3}).fillna(3)

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

# --- DATA FILTERING FOR VISUALIZATIONS ---

# Filtered data subset
filtered_data = df[['Gender', 'Year_of_Study', 'Current_Living_Situation', 
                    'Social_Media_Positive_Impact_on_Wellbeing', 
                    'Difficulty_Sleeping_University_Pressure', 'Race', 
                    'Social_Media_Daily_Routine', 'Employment_Status']].dropna()


# ====== SIDEBAR ======
with st.sidebar:
    st.title("Dashboard Controls")
    
    # --- Data Summary ---
    st.markdown("### 🧾 Data Summary")
    st.info(f"*Total Records:* {len(df):,}\n\n*Columns:* {len(df.columns)}")

    # --- Filters Section ---
    with st.expander("Filter Options", expanded=True):
        st.markdown("Select filters to refine your dashboard view:")

        # --- Multi-select Filters ---
        # --- Gender ---
        gender_filter = st.multiselect(
            "Gender",
            options=sorted(df["Gender"].dropna().unique()),
            default=sorted(df["Gender"].dropna().unique())
        )

        # --- Year of Study ---
        year_filter = st.multiselect(
            "Year of Study",
            options=sorted(df["Year_of_Study"].dropna().unique()),
            default=sorted(df["Year_of_Study"].dropna().unique())
        )

        # --- Programme ---
        programme_filter = st.multiselect(
            "Programme of Study",
            options=sorted(df["Programme_of_Study"].dropna().unique()),
            default=sorted(df["Programme_of_Study"].dropna().unique())
        )

        # --- Social Media Usage ---
        sm_filter = st.multiselect(
            "Social Media Usage (Hours / Day)",
            options=df["Social_Media_Use_Frequency"].cat.categories,
            default=df["Social_Media_Use_Frequency"].cat.categories
        )

        # --- Age Filter ---
        min_age, max_age = st.slider(
            "Age Range",
            int(df["Age"].min()),
            int(df["Age"].max()),
            (int(df["Age"].min()), int(df["Age"].max()))
        )

        # ===== APPLY FILTERS =====
        filtered_df = df.copy()
        filtered_numeric = df_numeric.copy()

        if gender_filter:
            filtered_df = filtered_df[filtered_df["Gender"].isin(gender_filter)]
            filtered_numeric = filtered_numeric.loc[filtered_df.index]

        if year_filter:
            filtered_df = filtered_df[filtered_df["Year_of_Study"].isin(year_filter)]
            filtered_numeric = filtered_numeric.loc[filtered_df.index]

        if programme_filter:
            filtered_df = filtered_df[filtered_df["Programme_of_Study"].isin(programme_filter)]
            filtered_numeric = filtered_numeric.loc[filtered_df.index]

        if sm_filter:
            filtered_df = filtered_df[filtered_df["Social_Media_Use_Frequency"].isin(sm_filter)]
            filtered_numeric = filtered_numeric.loc[filtered_df.index]

        filtered_df = filtered_df[
            (filtered_df["Age"] >= min_age) &
            (filtered_df["Age"] <= max_age)
        ]
        filtered_numeric = filtered_numeric.loc[filtered_df.index]
