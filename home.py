import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

def safe_corr(df, col_x, col_y):
    if col_x not in df.columns or col_y not in df.columns:
        return None
    temp = df[[col_x, col_y]].dropna()
    if len(temp) < 3:
        return None
    return temp.corr().iloc[0, 1]

def generate_scientific_summary(n, usage, stress, pos, neg):
    if n == 0:
        return "No data available under the current filter selection."

    impact_statement = (
        "negative wellbeing perceptions outweigh positive perceptions"
        if neg > pos else
        "positive wellbeing perceptions outweigh negative perceptions"
    )

    return (
        f"Based on the currently selected subgroup (n = {n}), students spend an "
        f"average of {usage:.1f} hours per day on social media. "
        f"The mean academic stress index is {stress:.2f}, indicating a moderate "
        f"level of perceived academic pressure. Notably, {impact_statement}, "
        f"suggesting that internet use is closely interrelated with students’ "
        f"mental wellbeing within this subgroup."
    )

def usage_summary(n, median_usage, high_usage_pct, study_hours):
    if n == 0:
        return "No data available for the selected filters."
    return (
        f"For the selected subgroup (n = {n}), the median social media usage "
        f"is {median_usage:.1f} hours per day. Approximately {high_usage_pct:.1f}% "
        f"of students are classified as high-usage users (≥5 hours/day). "
        f"Meanwhile, the average weekly study time is {study_hours:.1f} hours, "
        f"highlighting a potential imbalance between online engagement and academic commitment."
    )


def academic_summary(impact_pct, perf, high_users, study_hours):
    return (
        f"Approximately {impact_pct:.1f}% of students reported that social media "
        f"affects their academic studies. Despite this, the average academic "
        f"performance score is {perf:.2f}, suggesting moderate academic resilience. "
        f"Notably, {high_users:.1f}% of students belong to the high-usage group, "
        f"which may contribute to the perceived academic impact alongside an "
        f"average weekly study duration of {study_hours:.1f} hours."
    )


def wellbeing_summary(stress, sleep_pct, emotion, help_pct):
    return (
        f"The mental wellbeing analysis indicates a moderate average stress level "
        f"of {stress:.2f}. Approximately {sleep_pct:.1f}% of students reported "
        f"sleep disturbances linked to social media use. The emotional attachment "
        f"score of {emotion:.2f} reflects a noticeable emotional connection to online platforms, "
        f"while {help_pct:.1f}% of students seek online support during stressful periods."
    )


def correlation_summary(r_sm_stress, r_study_stress):
    return (
        f"The correlation analysis reveals a weak association between social media "
        f"usage duration and academic stress (r = {r_sm_stress:.2f}). Similarly, "
        f"study hours show a weak correlation with stress levels (r = {r_study_stress:.2f}), "
        f"suggesting that both digital engagement and academic workload contribute "
        f"incrementally to students’ stress experiences."
    )
    
# Bar Chart    
def bar_distribution_summary(counts, variable_name):
    if counts.sum() == 0:
        return f"No data available for {variable_name} under the current filters."

    dominant = counts.idxmax()
    dominant_pct = (counts.max() / counts.sum()) * 100

    return (
        f"The distribution of {variable_name.lower()} shows that "
        f"'{dominant}' is the most common category, accounting for "
        f"{dominant_pct:.1f}% of the selected respondents. This indicates "
        f"a dominant behavioural pattern within the current subgroup."
    )

# Boxplot
def boxplot_summary(df, x_col, y_col):
    if df.empty:
        return "Insufficient data to compare groups under the current filters."

    group_means = df.groupby(x_col)[y_col].mean().dropna()
    if group_means.empty:
        return "No valid numeric data available for comparison."

    highest = group_means.idxmax()
    lowest = group_means.idxmin()

    return (
        f"Group-wise comparison indicates that '{highest}' exhibits the highest "
        f"average {y_col.replace('_', ' ').lower()}, while '{lowest}' shows the lowest. "
        f"This suggests meaningful variation across groups."
    )

# Histogram/Likert 
def likert_summary(series, agree_levels=("Agree", "Strongly Agree")):
    if series.empty:
        return "No responses available under the current filter selection."

    agree_pct = series.isin(agree_levels).mean() * 100

    return (
        f"Approximately {agree_pct:.1f}% of respondents agree or strongly agree "
        f"with this statement, indicating a generally positive endorsement "
        f"within the selected subgroup."
    )

# Pie/Donut Chart
def pie_summary(counts):
    if counts.sum() == 0:
        return "No responses available for this question."

    dominant = counts.idxmax()
    dominant_pct = (counts.max() / counts.sum()) * 100

    return (
        f"The majority of respondents selected '{dominant}', representing "
        f"{dominant_pct:.1f}% of the total responses. This reflects the dominant "
        f"perception under the current filters."
    )

# Radar Chart
def radar_summary(values, labels):
    max_idx = values.index(max(values))
    min_idx = values.index(min(values))

    return (
        f"The radar profile indicates that '{labels[max_idx]}' represents the "
        f"most prominent wellbeing concern, while '{labels[min_idx]}' shows "
        f"relatively lower impact. This highlights key dimensions driving "
        f"mental health outcomes."
    )

def bar_chart_summary(df, col):
    if df.empty:
        return "No data available."
    counts = df[col].value_counts(normalize=True) * 100
    max_cat = counts.idxmax()
    min_cat = counts.idxmin()
    return (
        f"The bar chart shows the distribution of {col}. "
        f"Most respondents belong to '{max_cat}' ({counts[max_cat]:.1f}%), "
        f"while the least is '{min_cat}' ({counts[min_cat]:.1f}%). "
        f"This suggests a skewed distribution in {col} among the respondents."
    )

def box_plot_summary(df, col):
    if df.empty:
        return "No data available."
    median = df[col].median()
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    outliers = df[col][(df[col] < q1 - 1.5*(q3-q1)) | (df[col] > q3 + 1.5*(q3-q1))]
    return (
        f"The box plot for {col} shows a median of {median:.2f}, "
        f"with the interquartile range between {q1:.2f} and {q3:.2f}. "
        f"There are {len(outliers)} outlier(s), indicating occasional extreme responses."
    )

def scatter_plot_summary(df, x_col, y_col):
    if df.empty:
        return "No data available."
    corr = df[[x_col, y_col]].corr().iloc[0,1]
    direction = "positive" if corr > 0 else "negative"
    strength = "weak" if abs(corr)<0.3 else "moderate" if abs(corr)<0.6 else "strong"
    return (
        f"The scatter plot shows the relationship between {x_col} and {y_col}. "
        f"The correlation is {corr:.2f}, indicating a {strength} {direction} relationship. "
        f"Clusters or trends may suggest patterns worth investigating."
    )
def parallel_chart_summary(df, cols):
    if df.empty:
        return "No data available."
    means = df[cols].mean()
    highest = means.idxmax()
    lowest = means.idxmin()
    return (
        f"The parallel coordinates plot visualizes trends across {', '.join(cols)}. "
        f"On average, '{highest}' has the highest values ({means[highest]:.2f}) "
        f"while '{lowest}' has the lowest ({means[lowest]:.2f}), "
        f"indicating which attributes dominate overall patterns."
    )

def heatmap_summary(df, cols):
    if df.empty:
        return "No data available."
    corr = df[cols].corr()
    max_pair = corr.unstack().sort_values(ascending=False).drop_duplicates().iloc[1] # skip 1=diagonal 1.0
    max_cols = corr.unstack().sort_values(ascending=False).drop_duplicates().index[1]
    return (
        f"The heatmap shows correlations among {', '.join(cols)}. "
        f"The strongest relationship is between '{max_cols[0]}' and '{max_cols[1]}' "
        f"with a correlation of {max_pair:.2f}, indicating a notable positive association."
    )

def waterfall_summary(df, col, value_col):
    """
    df: dataframe containing the waterfall data
    col: categorical column for steps (e.g., categories)
    value_col: numeric column for the amounts
    """
    if df.empty:
        return "No data available."
    if col not in df.columns or value_col not in df.columns:
        return f"Columns '{col}' or '{value_col}' not found in the dataframe."

    # Group by category and sum values
    grouped = df.groupby(col)[value_col].sum()
    total_change = grouped.sum()
    max_step = grouped.idxmax()
    min_step = grouped.idxmin()
    
    return (
        f"The waterfall chart shows incremental changes in '{value_col}' across '{col}'. "
        f"The total net change is {total_change:.2f}. "
        f"The largest positive change is in '{max_step}', "
        f"while the largest negative change is in '{min_step}'."
    )


# --- MAIN TITLE ---
st.title(" Student Mental Health Monitoring Insights Dashboard")
st.markdown("Exploring the Relationship Between Internet Use and Mental Health.")

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Internet Use and Mental Health Dashboard",
    page_icon="🧠",
    layout="wide"
)

# banner
st.image(
    "banner.jpeg",
    use_container_width=True,
    caption="Internet Use and Mental Health Dashboard"
)

# --- LOAD DATA ---
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQnrGG72xRS-qLoiM2zon4eP8t5XMiO5MhoLUEe2jJer0G5EzodiU4e0NOmx_ssmCwZf-AnbQXhBbTM/pub?gid=1791189796&single=true&output=csv"
    return pd.read_csv(url)

df = load_data()

# Clean Column Names
df.columns = df.columns.str.strip()

# Rename Columns
df = df.rename(columns={
    "Age / Umur:": "Age",
    "Gender / Jantina:": "Gender",
    "Race / Bangsa:": "Race",
    "Year of Study / Tahun Belajar:": "Year_of_Study",
    "Programme of Study / Program Pembelajaran (cth., SST):": "Programme_of_Study",
    "Current living situation / Keadaan hidup sekarang:": "Current_Living_Situation",
    "Employment Status / Status Pekerjaan:": "Employment_Status",
    "Relationship Status / Status Perhubungan:": "Relationship_Status",
    "How would you describe your general academic performance? / Bagaimanakah anda menerangkan prestasi akademik umum anda?": "General_Academic_Performance",
    "How many hours do you study per week (outside class)? / Berapa jam anda belajar setiap minggu (di luar kelas)?": "Hours_Study_per_Week",
    "How often do you use social media? / Berapa kerap anda menggunakan media sosial?": "Social_Media_Use_Frequency",
    "Platforms you use most often (select all) / Platform yang paling kerap anda gunakan (pilih semua):": "Platforms_Most_Often_Used",
    "I have been feeling stressed or overwhelmed with assignments. / Saya telah berasa tertekan atau terbeban dengan tugasan.": "Assignments_Stress",
    "I often feel anxious about my academic workload. / Saya sering berasa bimbang tentang beban kerja akademik saya.": "Academic_Workload_Anxiety",
    "I have difficulty sleeping due to university-related pressure. / Saya sukar tidur kerana tekanan berkaitan universiti.": "Difficulty_Sleeping_University_Pressure",
    "I feel supported by friends or family when I am stressed. / Saya berasa disokong oleh rakan atau keluarga apabila saya tertekan.": "Friends_Family_Support",
    "I can manage my emotions well during stressful periods. / Saya boleh menguruskan emosi saya dengan baik semasa tempoh tekanan.": "Manage_Emotion_Stressful_Periods",
    "I use social media to relax or escape from academic stress. / Saya menggunakan media sosial untuk berehat atau melarikan diri daripada tekanan akademik.": "Social_Media_Relaxation",
    "I feel emotionally connected to my social media accounts. / Saya berasa tersambung secara emosi dengan akaun media sosial saya.": "Emotional_Connection_Social_Media",
    "Using social media is an important part of my daily routine. / Menggunakan media sosial adalah bahagian penting dalam rutin harian saya.": "Social_Media_Daily_Routine",
    "I sometimes lose track of time when using social media. / Saya kadang-kadang terlepas masa apabila menggunakan media sosial.": "Social_Media_Waste_Time",
    "Social media has affected my sleep (sleeping late or difficulty sleeping). / Media sosial telah menjejaskan tidur saya (tidur lewat atau sukar tidur).": "Sleep_Affected_By_Social_Media",
    "Social media affects my ability to concentrate on studies. / Media sosial menjejaskan keupayaan saya untuk menumpukan perhatian kepada pelajaran.": "Studies_Affected_By_Social_Media",
    "I use the Internet to look for mental health information (e.g., coping tips, stress-relief content). / Saya menggunakan Internet untuk mencari maklumat kesihatan mental (cth., petua mengatasi tekanan, kandungan melegakan tekanan).": "Mental_Health_Info_Through_Internet",
    "I have come across upsetting or disturbing content online. / Saya telah menemui kandungan yang menjengkelkan atau mengganggu dalam talian.": "Across_Upsetting_Content_Online",
    "When I feel stressed, I prefer to seek help online rather than talk to someone in person. / Apabila saya berasa tertekan, saya lebih suka mencari bantuan dalam talian daripada bercakap dengan seseorang secara peribadi.": "Seek_Help_Online_When_Stress",
    "I know where to find reliable mental health information online. / Saya tahu di mana untuk mencari maklumat kesihatan mental yang boleh dipercayai dalam talian.": "Find_Mental_Health_Info_Online",
    "I follow accounts that post motivational or mental health content. / Saya mengikuti akaun yang menyiarkan kandungan motivasi atau kesihatan mental.": "Follow_Motivational_Mental_Health_Content",
    "I use online communities for academic or emotional support. / Saya menggunakan komuniti dalam talian untuk sokongan akademik atau emosi.": "Use_Online_Communities_for_Support",
    "Social media has a generally positive impact on my wellbeing. / Media sosial secara amnya mempunyai kesan positif terhadap kesejahteraan saya.": "Social_Media_Positive_Impact_on_Wellbeing",
    "Social media has a generally negative impact on my wellbeing. / Media sosial secara amnya mempunyai kesan negatif terhadap kesejahteraan saya.": "Social_Media_Negative_Impact_on_Wellbeing",
    "Do you think universities should provide more online mental health resources? / Adakah anda fikir universiti harus menyediakan lebih banyak sumber kesihatan mental dalam talian?": "Do you think universities should provide more online mental health resources?",
    "What type of online content affects you the most (positive or negative)? / Apakah jenis kandungan dalam talian yang paling mempengaruhi anda (positif atau negatif)?": "Type_of_Online_Content_Affects",
    "What do you think universities can do to support student wellbeing? / Pada pendapat anda, apakah yang boleh dilakukan oleh universiti untuk menyokong kesejahteraan pelajar?": "Universities_Support_Actions"
})

# ================= OVERALL (UNFILTERED) DISTRIBUTION =================
st.header("Overall Social Media Usage (All Respondents)")

# ------ DATASET OVERVIEW ------
st.subheader("📋 Dataset Overview")

st.markdown("""
This section provides an **overall overview of the survey dataset** collected from UMK students.
It allows users to understand the **structure, size, and completeness** of the data before any
filtering or visualization is applied.
""")

# --- SUMMARY BOX ---
col1, col2, col3, col4 = st.columns(4)

top_academic = df['General_Academic_Performance'].mode()[0]
top_media = df['Social_Media_Use_Frequency'].mode()[0]

if not df.empty:
    col1.metric("Total Records", f"{len(df):,}", help="PLO 1: Total Respondent Records of Student", border=True)
    col2.metric("Avg. Age", f"{df['Age'].mean():.1f} years", help="PLO 2: Students Age", border=True)
    col3.metric("Academic Performance", top_academic, help="PLO 3: Students Academic Performance", border=True)
    col4.metric("Social Media Usage", top_media, help="PLO 4: Social Media Use Frecuency", border=True)
else:
    col1.metric("Total Records", "0", help="No data available")
    col2.metric("Avg. Age", "N/A", help="No data available")
    col3.metric("Academic Performance", "N/A", help="No data available")
    col4.metric("Social Media Usage", "N/A", help="No data available")

# --- Dataset Preview ---
with st.expander("View Dataset Preview"):
    st.dataframe(df.head(20), use_container_width=True)

st.markdown("---")

overall_counts = df["Social_Media_Use_Frequency"].value_counts(sort=False)

fig_overall = px.bar(
    x=overall_counts.index,
    y=overall_counts.values,
    labels={
        "x": "Hours per Day",
        "y": "Number of Students"
    },
    title="Overall Distribution of Daily Social Media Usage",
    color=overall_counts.index,
    color_discrete_sequence=px.colors.qualitative.Set2
)

fig_overall.update_layout(xaxis_tickangle=-30)
st.plotly_chart(fig_overall, use_container_width=True)

st.info(
    "This chart represents the **entire respondent population** without any filters applied. "
    "It serves as a baseline for comparison with filtered subgroup analyses."
)

st.markdown("---")

# Fix encoding issues
df = df.replace({"â\x80\x93": "-", "–": "-", "—": "-"}, regex=True)

# Drop Irrelevant Columns
cols_to_drop = [
    "Timestamp",
    "Type_of_Online_Content_Affects",
    "Universities_Support_Actions"
]

df = df.drop(columns=cols_to_drop, errors="ignore")
df_numeric = df.copy()

# ============ INDIVIDUAL PART FILTERING AND MAPPING ============
# ----------- AISHAH SAKINAH -----------

# Likert-scale columns (1–5)
LIKERT_COLS = [
    'Assignments_Stress',
    'Academic_Workload_Anxiety',
    'Difficulty_Sleeping_University_Pressure',
    'Friends_Family_Support',
    'Manage_Emotion_Stressful_Periods',
    'Social_Media_Relaxation',
    'Emotional_Connection_Social_Media',
    'Social_Media_Daily_Routine',
    'Social_Media_Waste_Time',
    'Sleep_Affected_By_Social_Media',
    'Studies_Affected_By_Social_Media',
    'Seek_Help_Online_When_Stress',
    'Social_Media_Positive_Impact_on_Wellbeing',
    'Social_Media_Negative_Impact_on_Wellbeing'
]


# Numeric Likert Columns
for col in LIKERT_COLS:
    if col in df_numeric.columns:
        df_numeric[col + "_Numeric"] = pd.to_numeric(
            df_numeric[col],
            errors="coerce"
        )

# Frequency-scale columns (1–4)
FREQ_COLS = [
    'Mental_Health_Info_Through_Internet',
    'Use_Online_Communities_for_Support',
    'Across_Upsetting_Content_Online'
]

# Frequency mapping
freq_map = {
    "Never": 1,
    "Rarely": 2,
    "Sometimes": 3,
    "Often": 4
}

# Frequency (1–4)
for col in FREQ_COLS:
    if col in df_numeric.columns:
        df_numeric[col + "_Numeric"] = (
            df_numeric[col].astype(str).str.strip().map(freq_map)
        )
    
# Study hours
df_numeric["Study_Hours_Numeric"] = df_numeric["Hours_Study_per_Week"].map({
    "Less than 5 hours": 2.5,
    "5 to 10 hours": 7.5,
    "11 to 15 hours": 13,
    "16 to 20 hours": 18,
    "More than 20 hours": 22.5
})

# Social media hours
df_numeric["Social_Media_Hours_Numeric"] = df_numeric["Social_Media_Use_Frequency"].map({
    "Less than 1 hour per day": 0.5,
    "1 to 2 hours per day": 1.5,
    "3 to 4 hours per day": 3.5,
    "5 to 6 hours per day": 5.5,
    "More than 6 hours per day": 7
})

# Academic performance mapping
academic_map = {
    "Below Average": 1,
    "Average": 2,
    "Good": 3,
    "Excellent": 4
}

# Academic performance numeric
df_numeric["General_Academic_Performance_Numeric"] = (
    df_numeric["General_Academic_Performance"]
    .astype(str)
    .str.strip()
    .replace({
        "Excellent ": "Excellent",
        "Good ": "Good"
    })
    .map(academic_map)
)

# Academic Stress Index
df_numeric["Academic_Stress_Index"] = df_numeric[
    [
        "Assignments_Stress_Numeric",
        "Academic_Workload_Anxiety_Numeric",
        "Difficulty_Sleeping_University_Pressure_Numeric"
    ]
].mean(axis=1)

# ----- CATEGORICAL ORDER -----
USAGE_ORDER = [
    "< 1 hr",
    "1–2 hrs",
    "3–4 hrs",
    "5–6 hrs",
    "> 6 hrs"
]

HIGH_USAGE = ["5–6 hrs", "> 6 hrs"]

df["Social_Media_Use_Frequency"] = df["Social_Media_Use_Frequency"].map({
    "Less than 1 hour per day": "< 1 hr",
    "1 to 2 hours per day": "1–2 hrs",
    "3 to 4 hours per day": "3–4 hrs",
    "5 to 6 hours per day": "5–6 hrs",
    "More than 6 hours per day": "> 6 hrs"
})

df["Social_Media_Use_Frequency"] = pd.Categorical(
    df["Social_Media_Use_Frequency"],
    categories=USAGE_ORDER,
    ordered=True
)

# ----------- ILYA -----------
# Re-apply short label mapping to 'Social_Media_Use_Frequency'
short_label_map_for_df = {
    "Less than 1 hour per day": "< 1 hr",
    "1 to 2 hours per day": "1–2 hrs",
    "3 to 4 hours per day": "3–4 hrs",
    "5 to 6 hours per day": "5–6 hrs",
    "More than 6 hours per day": "> 6 hrs"
}
df["Social_Media_Use_Frequency"] = df["Social_Media_Use_Frequency"].map(short_label_map_for_df)

# Create df_for_analysis by dropping the 'Platforms_Most_Often_Used' column
df_for_analysis = df.drop(columns=['Platforms_Most_Often_Used']).copy()

# Define numerical mapping for Social Media Use Frequency
social_media_hours_map = {
    "< 1 hr": 0.5,
    "1–2 hrs": 1.5,
    "3–4 hrs": 3.5,
    "5–6 hrs": 5.5,
    "> 6 hrs": 7
}
df_for_analysis["Daily_Internet_Usage_Hours"] = df_for_analysis["Social_Media_Use_Frequency"].map(social_media_hours_map)

# Define mental health related columns and convert them to numeric
mental_health_cols = [
    'Assignments_Stress',
    'Academic_Workload_Anxiety',
    'Difficulty_Sleeping_University_Pressure',
    'Social_Media_Negative_Impact_on_Wellbeing'
]

for col in mental_health_cols:
    df_for_analysis[col] = pd.to_numeric(df_for_analysis[col])

# Map mental health factor names for better legend readability
mental_health_factor_map = {
    'Assignments_Stress': 'Stress from Assignments',
    'Academic_Workload_Anxiety': 'Academic Workload Anxiety',
    'Difficulty_Sleeping_University_Pressure': 'Difficulty Sleeping (Pressure)',
    'Social_Media_Negative_Impact_on_Wellbeing': 'Negative Social Media Impact'
}

df_for_analysis['Mental_Health_Factor'] = df_for_analysis[mental_health_cols].apply(
    lambda row: mental_health_factor_map.get(row.name), axis=1
)

# Melt the DataFrame for easier plotting with Plotly
df_melted = df_for_analysis.melt(
    id_vars=['Daily_Internet_Usage_Hours'],
    value_vars=mental_health_cols,
    var_name='Mental_Health_Factor',
    value_name='Score'
)

df_melted['Mental_Health_Factor'] = df_melted['Mental_Health_Factor'].map(mental_health_factor_map)

# Group by internet usage and mental health factor, then calculate the mean score
df_grouped = df_melted.groupby(['Daily_Internet_Usage_Hours', 'Mental_Health_Factor'])['Score'].mean().reset_index()

# ----------- HANIS NABILA -----------
# ----------- AINUN -----------

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

        # --- Gender ---
        gender_filter = st.multiselect(
            "Gender",
            options=sorted(df["Gender"].dropna().unique()),
            default=[]
        )

        # --- Year of Study ---
        year_filter = st.multiselect(
            "Year of Study",
            options=sorted(df["Year_of_Study"].dropna().unique()),
            default=[]
        )

        # --- Programme ---
        programme_filter = st.multiselect(
            "Programme of Study",
            options=sorted(df["Programme_of_Study"].dropna().unique()),
            default=[]
        )

        # --- Social Media Usage ---
        sm_filter = st.multiselect(
            "Social Media Usage (Hours / Day)",
            options=list(df["Social_Media_Use_Frequency"].cat.categories),
            default=[]
        )

        # --- Age Filter (KEEP THIS) ---
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
        
        # ===== REAL-TIME SUMMARY CALCULATIONS =====
        sample_size = len(filtered_df)

        avg_usage = filtered_numeric["Social_Media_Hours_Numeric"].mean()
        avg_stress = filtered_numeric["Academic_Stress_Index"].mean()
        avg_positive = filtered_numeric["Social_Media_Positive_Impact_on_Wellbeing_Numeric"].mean()
        avg_negative = filtered_numeric["Social_Media_Negative_Impact_on_Wellbeing_Numeric"].mean()


    # --- Reset and Download Buttons ---
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Reset Filters"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    with col2:
        st.download_button(
            label="Download CSV",
            data=filtered_df.to_csv(index=False).encode("utf-8"),
            file_name="students_data.csv",
            mime="text/csv"
        )
    st.markdown("---")

# ===== THEME TOGGLE =====
theme_mode = st.sidebar.radio("Select Theme Mode", ["Light 🌞", "Dark 🌙"], horizontal=True)

if theme_mode == "Dark 🌙":
    st.markdown("""
        <style>
        body { background-color: #121212; color: white; }
        [data-testid="stSidebar"] { background-color: #1E1E1E; color: white; }
        .stMetric, .stPlotlyChart, .stMarkdown { color: white !important; }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        body { background-color: #FAFAFA; color: black; }
        [data-testid="stSidebar"] { background-color: #FFFFFF; color: black; }
        </style>
    """, unsafe_allow_html=True)

# ===== COLOR THEME =====
COLOR_SEQ = px.colors.qualitative.Set2
CONTINUOUS_SCALE = "RdYlBu_r"


# --- TAB LAYOUT ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Internet Use vs. Mental Health", "Ilya", "Help-Seeking Behavior", "Ainun"])

# ============ INDIVIDUAL PART VISUALIZATION ============
# ----------- AISHAH SAKINAH -----------

# ============ TAB 1: INTERNET USE VS. MENTAL HEALTH ============
with tab1:
    st.subheader("Internet Use & Mental Health Insights")
    st.markdown("Analyzing interrelationships between social media usage, academic stress, and student wellbeing.")

    # Summary box
    col1, col2, col3, col4 = st.columns(4)
    valid_stress = filtered_numeric["Academic_Stress_Index"].dropna()

    col1.metric("Total Students", f"{len(filtered_df):,}", border=True)
    col2.metric("Avg. Age", f"{filtered_df['Age'].mean():.1f}", border=True)
    if not valid_stress.empty:
        col3.metric("Avg. Stress Index", f"{valid_stress.mean():.2f}", border=True)
    else:
        col3.metric("Avg Stress Index", "N/A", help="No valid stress index data after filtering", border=True)
    col4.metric("High Usage (%)", f"{(filtered_df['Social_Media_Use_Frequency'].isin(['5 to 6 hours per day', 'More than 6 hours per day']).mean() * 100):.1f}%", border=True)

    # Scientific Summary
    # ===== REAL-TIME SCIENTIFIC SUMMARY =====
    st.markdown("### Real-Time Scientific Summary")

    st.info(
        generate_scientific_summary(
            sample_size,
            avg_usage,
            avg_stress,
            avg_positive,
            avg_negative
        )
    )

    st.markdown("---")

    # --- TAB LAYOUT ---
    usage_tab, academic_tab, wellbeing_tab, insight_tab = st.tabs(["📉 Usage Patterns", "🎓 Academic Impact", "📈 Wellbeing Analysis", "🗺️ Correlation & Advanced Insights"])
    
    # ============ TAB 1.1: USAGE PATTERNS ============
    with usage_tab:
        st.subheader("Internet & Social Media Usage Patterns")
        st.markdown("Understand how much and how often students use the internet/social media.")

        # Summary box
        freq_order = df["Social_Media_Use_Frequency"].cat.categories
        median_usage = filtered_numeric["Social_Media_Hours_Numeric"].median()
        high_usage_pct = (filtered_df["Social_Media_Use_Frequency"].isin(HIGH_USAGE).mean() * 100)
        avg_study_hours = filtered_numeric["Study_Hours_Numeric"].mean()
        time_waste_pct = (filtered_df["Social_Media_Waste_Time"].isin(["Agree", "Strongly Agree"]).mean() * 100)
        usage_counts = (filtered_df["Social_Media_Use_Frequency"].value_counts().reindex(USAGE_ORDER, fill_value=0))
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Median Social Media Hours/Day", f"{median_usage:.1f} hrs" if pd.notna(median_usage) else "N/A", help="Typical daily social media usage (median)", border=True)
        col2.metric("High Usage Group (%)", f"{high_usage_pct:.1f}%", help="Students using 5 hours or more per day", border=True)
        col3.metric("Avg. Study Hours/Week", f"{avg_study_hours:.1f}" if pd.notna(median_usage) else "N/A", help="Average academic study commitment", border=True)
        col4.metric("Perceived Time Loss (%)", f"{time_waste_pct:.1f}%", help="Students who feel social media wastes their time", border=True)
        
        # Scientific Summary
        st.markdown("### Real-Time Usage Summary")

        st.info(
            usage_summary(
                len(filtered_df),
                filtered_numeric["Social_Media_Hours_Numeric"].median(),
                (filtered_df["Social_Media_Use_Frequency"]
                 .isin(HIGH_USAGE)
                 .mean() * 100),
                filtered_numeric["Study_Hours_Numeric"].mean()
            )
        )

        st.markdown("---")
        
        # Bar Chart
        fig = px.bar(
            x=usage_counts.index,
            y=usage_counts.values,
            labels={
                "x": "Daily Social Media Usage",
                "y": "Number of Students"
            },
            title="Distribution of Daily Social Media Usage",
            color_discrete_sequence=px.colors.qualitative.Set2
        )

        fig.update_layout(xaxis_tickangle=-30)
        st.plotly_chart(fig, use_container_width=True)

        st.info(
            bar_distribution_summary(
                usage_counts,
                "Daily Social Media Usage"
            )
        )

        st.markdown("---")
            
        # Bar Chart
        study_order = [
            "Less than 5 hours", "5 to 10 hours",
            "11 to 15 hours", "16 to 20 hours", "More than 20 hours"
        ]

        fig = px.bar(
            filtered_df["Hours_Study_per_Week"].value_counts().reindex(study_order),
            title="Frequency of Study Hours per Week",
            labels={"value": "Number of Students", "index": "Study Hours"},
            color_discrete_sequence=px.colors.qualitative.Pastel
        )

        fig.update_layout(xaxis_tickangle=-25)
        st.plotly_chart(fig, use_container_width=True)
        usage_counts = filtered_df["Social_Media_Use_Frequency"].value_counts()
        dominant_group = usage_counts.idxmax()

        study_counts = (filtered_df["Hours_Study_per_Week"].value_counts().reindex(study_order, fill_value=0))

        st.info(
            bar_distribution_summary(
                study_counts,
                "Weekly Study Hours"
            )
        )

        # Box Plot
        fig = px.box(
            filtered_df,
            x="Gender",
            y="Social_Media_Use_Frequency",
            title="Social Media Usage by Gender",
            color="Gender",
            color_discrete_sequence=px.colors.qualitative.Safe
        )

        st.plotly_chart(fig, use_container_width=True)
        st.info(
            boxplot_summary(
                filtered_numeric,
                "Gender",
                "Social_Media_Hours_Numeric"
            )
        )


        # Histogram
        fig = px.histogram(
            filtered_df,
            title="Perception of Wasting Time on Social Media",
            x="Social_Media_Waste_Time",
            color_discrete_sequence=COLOR_SEQ,
            category_orders={"Social_Media_Waste_Time": [
            "Strongly Disagree","Disagree","Neutral","Agree","Strongly Agree"
            ]}
        )

        fig.update_layout(
            xaxis_title="Response Level",
            yaxis_title="Number of Students",
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)
        st.info(
            likert_summary(
                filtered_df["Social_Media_Waste_Time"]
            )
        )

        # Pie Donut
        resource_counts = filtered_df[
            'Do you think universities should provide more online mental health resources?'
        ].value_counts().reset_index()

        resource_counts.columns = ["Response", "Count"]

        fig = px.pie(
            resource_counts,
            names="Response",
            values="Count",
            hole=0.45,
            color_discrete_sequence=COLOR_SEQ,
            title="Need for Online Mental Health Resources"
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)

        resource_counts = filtered_df[
            "Do you think universities should provide more online mental health resources?"
        ].value_counts()

        st.info(
            pie_summary(resource_counts)
        )
       
        st.markdown("#### 💬 Key Insights")
        st.info(
            "Students exhibit varying social media usage patterns. The majority use social media "
            "moderately (1–4 hours/day), while a notable subgroup spends 5+ hours daily. "
            "High-usage students report higher perceptions of time wasted online, and their "
            "average study hours tend to be lower, highlighting a potential trade-off between "
            "online engagement and academic commitment."
        )

    
    # ============ TAB 1.2: ACADEMIC IMPACT ============
    with academic_tab:
        st.subheader("Academic Impact of Social Media Analysis")
        st.markdown("Examine whether internet usage affects academic outcomes.")

        # Summary box
        col1, col2, col3, col4 = st.columns(4)
        study_impact = filtered_numeric["Studies_Affected_By_Social_Media_Numeric"].dropna()
        academic_perf = filtered_numeric["General_Academic_Performance_Numeric"].dropna()
        study_hours = filtered_numeric["Study_Hours_Numeric"].dropna()
        high_users_pct = (filtered_df["Social_Media_Use_Frequency"].isin(["5 to 6 hours per day", "More than 6 hours per day"]).mean() * 100)
        sleep_pct = (filtered_numeric["Sleep_Affected_By_Social_Media_Numeric"] >= 4).mean() * 100
        corr_val = safe_corr(filtered_numeric, "Social_Media_Hours_Numeric", "Assignments_Stress_Numeric")
    
        col1.metric("Study Impact (%)", f"{(study_impact.mean()/5*100):.1f}%" if not study_impact.empty else "N/A", help="Average perceived impact of social media on studies", border=True)
        col2.metric("Avg. Academic Performance", f"{academic_perf.mean():.2f}" if not academic_perf.empty else "N/A", help="Numeric scale: 1=Below Avg → 4=Excellent", border=True)
        col3.metric("High Usage Students (%)", f"{high_users_pct:.1f}%", help="Students using ≥5 hours/day", border=True)
        col4.metric("Avg. Weekly Study Hours", f"{study_hours.mean():.1f}" if not study_hours.empty else "N/A", help="Self-reported weekly study time", border=True)
        
        # Scientific Summary
        st.markdown("### Real-Time Academic Impact Summary")

        st.info(
            academic_summary(
                (study_impact.mean()/5*100),
                academic_perf.mean(),
                high_users_pct,
                study_hours.mean()
            )
        )


        st.markdown("---")

        # Bar Chart
        academic_numeric = filtered_numeric.dropna(
            subset=["Academic_Stress_Index"]
        )


        usage_group_mean = (
            filtered_numeric
            .groupby("Social_Media_Use_Frequency", observed=True)
            ["Academic_Stress_Index"]
            .mean()
            .reset_index()
        )

        fig = px.bar(
            usage_group_mean,
            x="Social_Media_Use_Frequency",
            y="Academic_Stress_Index",
            title="Academic Stress vs Social Media Usage",
            color="Academic_Stress_Index",
            color_continuous_scale=CONTINUOUS_SCALE
        )

        fig.update_layout(
            xaxis_title="Social Media Usage",
            yaxis_title="Academic Stress Index",
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)
        mean_stress = usage_group_mean["Academic_Stress_Index"].mean()

        st.info(bar_chart_summary(filtered_df, "Social_Media_Use_Frequency"))

        
        # Box Plot
        fig = px.box(
            df,
            x="Social_Media_Use_Frequency",
            y="General_Academic_Performance",
            title="Social Media Frequency vs Academic Performance",
            color="Social_Media_Use_Frequency",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig, use_container_width=True)
        st.info(box_plot_summary(filtered_numeric, "General_Academic_Performance_Numeric"))

        # Box Plot
        fig = px.box(
            df_numeric,
            x="Social_Media_Use_Frequency",
            y="Sleep_Affected_By_Social_Media",
            color="Social_Media_Use_Frequency",
            color_discrete_sequence=COLOR_SEQ
        )

        fig.update_layout(
            title="Sleep Disturbance by Social Media Usage",
            xaxis_title="Usage Frequency",
            yaxis_title="Sleep Affected Score",
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.info(box_plot_summary(filtered_numeric, "Sleep_Affected_By_Social_Media_Numeric"))

        # Scatter Plot
        fig = px.scatter(
            df,
            x="Age",
            y="Studies_Affected_By_Social_Media",
            title="Age vs Impact of Social Media on Studies",
            color="Gender",
            opacity=0.7,
            color_discrete_sequence=px.colors.qualitative.Dark2
        )

        st.plotly_chart(fig, use_container_width=True)

        st.info(scatter_plot_summary(filtered_numeric, "Age", "Studies_Affected_By_Social_Media_Numeric"))

        st.markdown("#### 💬 Key Insights")
        st.info(
            "Higher social media usage is modestly associated with increased academic stress. "
            "Despite this, most students maintain moderate to good academic performance. "
            "High-usage students (≥5 hours/day) may require support to manage stress, "
            "and study habits appear to moderate the impact of social media on academic outcomes."
        )

    # ============ TAB 1.3: WELLBEING ANALYSIS ============
    with wellbeing_tab:
        st.subheader("Mental & Emotional Wellbeing")
        st.markdown("Understand stress, sleep, and emotional responses linked to online behaviour.")

        # Summary box
        col1, col2, col3, col4 = st.columns(4)
        stress = filtered_numeric["Assignments_Stress_Numeric"].dropna()
        sleep = filtered_numeric["Sleep_Affected_By_Social_Media_Numeric"].dropna()
        emotion = filtered_numeric["Emotional_Connection_Social_Media_Numeric"].dropna()
        help_seek = filtered_numeric["Seek_Help_Online_When_Stress_Numeric"].dropna()
        sleep_pct = (filtered_numeric["Sleep_Affected_By_Social_Media_Numeric"] >= 4).mean() * 100
    
        col1.metric("Avg. Stress Level", f"{stress.mean():.2f}" if not stress.empty else "N/A", border=True)
        col2.metric("Sleep Affected (%)", f"{(sleep.mean()/5*100):.1f}%" if not sleep.empty else "N/A", border=True)
        col3.metric("Emotional Attachment", f"{emotion.mean():.2f}" if not emotion.empty else "N/A", border=True)
        col4.metric("Online Help Seeking (%)", f"{(help_seek.mean()/5*100):.1f}%" if not help_seek.empty else "N/A", border=True)

        # Scientific Summary
        st.markdown("### Real-Time Wellbeing Summary")

        st.info(
            wellbeing_summary(
                stress.mean(),
                (sleep.mean()/5*100),
                emotion.mean(),
                (help_seek.mean()/5*100)
            )
        )

        st.markdown("---")


        # Radar / Polar Chart
        st.subheader("Mental Health Impact Profile")
            
        categories = [
            'Assignments_Stress',
            'Academic_Workload_Anxiety',
            'Difficulty_Sleeping_University_Pressure',
            'Sleep_Affected_By_Social_Media',
            'Studies_Affected_By_Social_Media'
        ]

        values = df_numeric[categories].mean().tolist()
 
        fig = go.Figure(
            go.Scatterpolar(
                r=values + [values[0]],
                theta=categories + [categories[0]],
                fill='toself',
                line_color="#636EFA"
            )
        )

        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[1,5])),
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)

        values = filtered_numeric[categories].mean().tolist()

        st.info(
            radar_summary(
                values,
                categories
            )
        )


        # Parallel coordinates
        cols_parallel = [
            'Assignments_Stress_Numeric',
            'Academic_Workload_Anxiety_Numeric',
            'Sleep_Affected_By_Social_Media_Numeric',
            'Studies_Affected_By_Social_Media_Numeric'
        ]

        parallel_df = filtered_numeric[cols_parallel].dropna()

        fig = px.parallel_coordinates(
            parallel_df,
            dimensions=cols_parallel,
            color='Assignments_Stress_Numeric',
            color_continuous_scale=CONTINUOUS_SCALE
        )
        fig.update_layout(template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
        st.info(parallel_chart_summary(filtered_numeric, cols_parallel))

       
        st.markdown("#### 💬 Key Insights")
        st.info(
            "Mental wellbeing patterns show moderate average stress levels across students. "
            "A substantial proportion report sleep disturbances linked to social media use. "
            "Emotional attachment to social media is noticeable, and many students seek online support "
            "during stressful periods, highlighting the importance of accessible mental health resources."
        )

    # ============ TAB 1.4: CORRELATION & INSIGHTS ============
    with insight_tab:
        st.subheader("Correlation & Deep Analysis")
        st.markdown("Reveal hidden relationships across variables (lecturer favourite).")

        # Summary box
        col1, col2, col3, col4 = st.columns(4)
        corr_sm_stress = safe_corr(filtered_numeric, "Social_Media_Hours_Numeric", "Assignments_Stress_Numeric")
        corr_study_stress = safe_corr(filtered_numeric, "Study_Hours_Numeric", "Assignments_Stress_Numeric")
        impact_gap = (
            filtered_numeric['Social_Media_Positive_Impact_on_Wellbeing_Numeric'].mean(skipna=True)
            -
            filtered_numeric['Social_Media_Negative_Impact_on_Wellbeing_Numeric'].mean(skipna=True)
        )
        support_score = filtered_numeric["Use_Online_Communities_for_Support_Numeric"].dropna()

        col1.metric("Social Media Hours ↔ Stress", f"{corr_sm_stress:.2f}" if corr_sm_stress is not None else "N/A", border=True)
        col2.metric("Study Hours ↔ Stress", f"{corr_study_stress:.2f}" if corr_sm_stress is not None else "N/A", border=True)
        col3.metric("Wellbeing Impact Gap", f"{impact_gap:.2f}", help="Positive = benefits outweigh harms", border=True)
        col4.metric("Support-Seeking Score", f"{support_score.mean():.2f}" if not support_score.empty else "N/A", border=True)

        # Scientific Summary
        st.markdown("### Real-Time Correlation Summary")

        if corr_sm_stress is not None and corr_study_stress is not None:
            st.info(
                correlation_summary(
                    corr_sm_stress,
                    corr_study_stress
                )
            )
        else:
            st.info("Insufficient data to compute correlations under the current filter selection.")

        st.markdown("---")

        # Heatmap
        corr = df_numeric[
            [
                'Assignments_Stress',
                'Academic_Workload_Anxiety',
                'Sleep_Affected_By_Social_Media',
                'Studies_Affected_By_Social_Media',
                'Social_Media_Hours_Numeric'
            ]
        ].corr()

        fig = px.imshow(
            corr,
            text_auto=".2f",
            color_continuous_scale=CONTINUOUS_SCALE
        )

        fig.update_layout(
            title="Correlation Between Internet Use & Mental Health",
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)
        st.info(heatmap_summary(filtered_numeric, cols_parallel))

        # Waterfall Chart
        mean_vals = df_numeric[
            [
                'Assignments_Stress',
                'Academic_Workload_Anxiety',
                'Sleep_Affected_By_Social_Media',
                'Studies_Affected_By_Social_Media'
            ]
        ].mean()

        fig = go.Figure(go.Waterfall(
            x=[
                "Assignments Stress",
                "Academic Anxiety",
                "Sleep Affected",
                "Studies Affected",
                "Overall Impact"
            ],
            y=[
                mean_vals[0],
                mean_vals[1],
                mean_vals[2],
                mean_vals[3],
                mean_vals.sum()
            ],
            measure=["relative","relative","relative","relative","total"]
        ))

        fig.update_layout(
            title="Cumulative Mental Health Impact",
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)
        st.info(waterfall_summary(filtered_numeric, col='Gender', value_col='Academic_Stress_Index'))
   
       
        st.markdown("#### 💬 Key Insights")
        st.info(
            "Correlation analysis reveals weak-to-moderate associations between social media usage, "
            "study hours, and academic stress. Positive wellbeing impacts slightly outweigh negative ones, "
            "and students who use online communities for support show higher engagement with coping strategies. "
            "These insights highlight areas for intervention and targeted support for high-usage or stressed students."
        )

# ----------- ILYA -----------

# ============ TAB 2: ILYA ============
with tab2:
    st.title("Relationship Between Internet Usage and Mental Health Outcomes")

    # Display a brief explanation of the project
    st.write("""
        This app explores the relationship between internet usage and mental health outcomes
        among UMK students, with visualizations showing correlations between internet usage
        and various mental health factors like stress, anxiety, and the impact of social media.
    """)

    # Display Plotly grouped bar chart
    st.subheader("Mental Health Scores by Internet Usage")
    fig = px.bar(
        df_grouped,
        x='Daily_Internet_Usage_Hours',
        y='Score',
        color='Mental_Health_Factor',
        barmode='group',
        labels={'Daily_Internet_Usage_Hours': 'Internet Usage (hours)', 'Score': 'Mental Health Score'},
        title="Mental Health Scores by Internet Usage"
    )

    st.plotly_chart(fig)

    # --- Box Plot ---
    # Create the box plot for "Difficulty Sleeping Due to University Pressure by Social Media Affecting Sleep"
    df_new = df.copy() # Re-load original dataset
    df_new['Sleep_Affected_By_Social_Media_Numeric_Str'] = df_new['Sleep_Affected_By_Social_Media'].astype(str)

    def map_sleep_impact_to_binary(response_str):
        try:
            response_int = int(response_str)
            if response_int >= 4: # Assuming 4 (Agree) and 5 (Strongly Agree) mean 'Yes'
                return 'Yes'
            elif response_int <= 3: # Assuming 1 (Strongly Disagree), 2 (Disagree), 3 (Neutral) mean 'No'
                return 'No'
        except ValueError: # Handle cases where conversion to int fails (e.g., non-numeric data)
            return None

    df_new['Internet_Use_Affects_Sleep'] = df_new['Sleep_Affected_By_Social_Media_Numeric_Str'].apply(map_sleep_impact_to_binary)

    df_new['Difficulty_Sleeping_University_Pressure_Score'] = pd.to_numeric(
        df_new['Difficulty_Sleeping_University_Pressure'],
        errors='coerce'
    )

    df_plot = df_new.dropna(subset=[
        'Internet_Use_Affects_Sleep',
        'Difficulty_Sleeping_University_Pressure_Score'
    ]).copy()

    fig_box = px.box(
        df_plot,
        x='Internet_Use_Affects_Sleep',
        y='Difficulty_Sleeping_University_Pressure_Score',
        points="all",
        labels={'Difficulty_Sleeping_University_Pressure_Score': 'Difficulty Sleeping Score'},
        title='Difficulty Sleeping Due to University Pressure by Social Media Affecting Sleep'
    )

    st.plotly_chart(fig_box)

    # --- Heatmap ---
    # Create correlation heatmap
    df_heatmap = df_numeric.copy()

    numerical_cols = ['Age', 'Social_Media_Hours_Numeric', 'Study_Hours_Numeric'] + \
                     [col for col in LIKERT_COLS if col in df_heatmap.columns and df_heatmap[col].dtype != 'object']

    correlation_matrix = df_heatmap[numerical_cols].dropna().corr()

    # Short names for better display
    short_names = {
        "Age": "Age",
        "Social_Media_Hours_Numeric": "SM Hours",
        "Study_Hours_Numeric": "Study Hours",
        "Assignments_Stress_Numeric": "Assignment Stress",
        "Academic_Workload_Anxiety_Numeric": "Workload Anxiety",
        "Difficulty_Sleeping_University_Pressure_Numeric": "Sleep Difficulty",
        "Sleep_Affected_By_Social_Media_Numeric": "Sleep Affected",
        "Studies_Affected_By_Social_Media_Numeric": "Study Affected",
        "Social_Media_Positive_Impact_on_Wellbeing_Numeric": "Positive Impact",
        "Social_Media_Negative_Impact_on_Wellbeing_Numeric": "Negative Impact",
        "Emotional_Connection_Social_Media_Numeric": "Emotional Attachment"
    }

    correlation_matrix_renamed = correlation_matrix.rename(
        index=short_names, columns=short_names
    )

    fig_heatmap = px.imshow(
        correlation_matrix_renamed,
        labels=dict(x="Variables", y="Variables", color="Correlation"),
        title="Correlation Heatmap",
        width=900,
        height=800
    )

    fig_heatmap.update_xaxes(tickangle=45)

    st.plotly_chart(fig_heatmap, use_container_width=True)

    # --- Line Plot: Mental Health Scores vs Internet Usage ---
    st.subheader("Daily Internet Usage vs Mean Mental Health Scores")

    # Prepare df_line
    df_line = df_melted.copy()
    df_line["Score"] = pd.to_numeric(df_line["Score"], errors="coerce")
    df_line["Daily_Internet_Usage_Hours"] = pd.to_numeric(df_line["Daily_Internet_Usage_Hours"], errors="coerce")
    df_line = df_line.dropna(subset=["Score", "Daily_Internet_Usage_Hours", "Mental_Health_Factor"])

    # Group and calculate mean
    df_grouped_line = (
        df_line.groupby(["Daily_Internet_Usage_Hours", "Mental_Health_Factor"])["Score"]
        .mean()
        .reset_index()
        .sort_values("Daily_Internet_Usage_Hours")
    )

    # Convert hours to string for faceting
    df_grouped_line['Daily_Internet_Usage_Hours_Str'] = df_grouped_line['Daily_Internet_Usage_Hours'].astype(str)

    # --- Plotly Line Plot ---
    fig_line = px.line(
        df_grouped_line,
        x='Daily_Internet_Usage_Hours_Str',
        y='Score',
        facet_col='Mental_Health_Factor',
        facet_col_wrap=2,
        markers=True,
        title='Daily Internet Usage vs Mean Mental Health Scores',
        labels={
            'Daily_Internet_Usage_Hours_Str': 'Daily Internet Usage (Hours per Day)',
            'Score': 'Mean Mental Health Score'
        }
    )
    fig_line.update_layout(template='plotly_white', height=600)
    fig_line.update_yaxes(dtick=1)
    st.plotly_chart(fig_line, use_container_width=True)

    # --- Seaborn Scatter Plots ---
    st.subheader("Scatter Plots: Daily Internet Usage vs Mental Health Scores")

    # Create a new figure to avoid Streamlit re-use errors
    plt.figure(figsize=(12, 8))

    g = sns.relplot(
        x='Daily_Internet_Usage_Hours',
        y='Score',
        col='Mental_Health_Factor',
        col_wrap=2,
        data=df_line,  # Use cleaned df_line
        kind='scatter',
        height=4,
        aspect=1.2,
        s=50,
        alpha=0.7
    )

    g.set_axis_labels("Daily Internet Usage (Hours)", "Mental Health Score")
    g.set_titles("{col_name}")

    # Adjust layout and title
    plt.suptitle('Daily Internet Usage vs Mental Health Scores', y=1.02)
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    # Render the plot in Streamlit
    st.pyplot(g.fig)  # Use g.fig instead of plt


# ----------- HANIS NABILA -----------
# ================= TAB 3: HANIS NABILA =================
with tab3:
    st.header("Analyze Mental Health Information-Seeking Behavior")

    # =====================================================
#   Online Help Preference (High vs Low)
# =====================================================
st.subheader("Preference for Online Help (High vs Low)")

df['Online_Help_Level'] = df['Seek_Help_Online_When_Stress'].astype(str).apply(
    lambda x: 'High (Agree)' if x in ['4','5'] else 'Low (Neutral)'
)

pie_data = df['Online_Help_Level'].value_counts().reset_index()
pie_data.columns = ['Preference', 'Count']

fig = px.pie(
    pie_data,
    names='Preference',
    values='Count',
    hole=0.45,
    title="Overall Preference for Seeking Help Online"
)

st.plotly_chart(fig, use_container_width=True)

st.success("""
**Interpretation:**  
The donut chart shows that a huge majority of students, 72.3%, stay in the low or neutral zone. 
Only 27.7% really prefer getting help online regarding this preference. It seems like some 
people really find digital platforms to be their go-to for support.

""")

# =====================================================
# ONLINE COMMUNITIES BY GENDER
# =====================================================
st.subheader("Online Community Support by Gender")

gender_table = pd.crosstab(
    df['Use_Online_Communities_for_Support'],
    df['Gender']
)

fig, ax = plt.subplots(figsize=(10, 6))
gender_table.plot(kind='bar', ax=ax)
ax.set_title("Use of Online Communities for Support by Gender")
ax.set_xlabel("Agreement Level")
ax.set_ylabel("Number of Students")
st.pyplot(fig)

st.success("""
**Interpretation:**  
Female students consistently outnumber male students across almost all frequency categories, 
most notably in the "Sometimes" category. "Often" category shows 15 female participants but 0 male participants.
This shows that frequent engagement with online support communities is almost exclusively a female behavior in this dataset.
""")

# =====================================================
#   Assignment Stress vs Online Help
# =====================================================
st.subheader("Assignment Stress vs Online Help Preference")

fig = px.box(
    df,
    x="Seek_Help_Online_When_Stress",
    y="Assignments_Stress",
    title="Assignment Stress Levels Across Online Help Preference",
    labels={
        "Seek_Help_Online_When_Stress": "Online Help Preference Level",
        "Assignments_Stress": "Assignment Stress Level"
    }
)

st.plotly_chart(fig, use_container_width=True)

st.success("""
**Interpretation:**  
The box plot shows that students who really want online help (Level 5) also have some of 
the highest stress levels, reaching up to level 5 on the stress scale. Meanwhile, those who 
do not need care for online help (Level 1) usually have lower stress. 
""")

# =====================================================
#   ONLINE INFO SEEKING
# =====================================================
st.subheader("Seeking Mental Health Information Online")

fig = px.histogram(
    df,
    x="Mental_Health_Info_Through_Internet",
    title="Frequency of Seeking Mental Health Information Online"
)
st.plotly_chart(fig, use_container_width=True)

st.success("""
**Interpretation:**  
This chart shows that shows that "Sometimes" is the most common frequency, with a count of 50. 
This is followed by "Rarely" (20) and "Often" (17). Notably, only a small fraction of the 
group "Always" (8) or "Never" (6) seeks out this information.
This indicates that while most students use the internet for mental health information, 
they do so sporadically rather than as a constant habit.
""")

# =====================================================
# ONLINE HELP WHEN STRESSED
# =====================================================
st.subheader("Preference for Online Help During Stress")

fig = px.histogram(
    df,
    x="Seek_Help_Online_When_Stress",
    title="Preference for Seeking Help Online When Stressed"
)
st.plotly_chart(fig, use_container_width=True)

st.success("""
**Interpretation:**  
The distribution is somewhat bell-shaped but leans toward the middle. The highest 
count is at Level 3 (35 students), indicating a moderate preference. This suggests 
that while students are open to online help when stressed, many maintain a neutral 
or cautious.
""")

# =====================================================
# STRESS vs ONLINE COMMUNITIES
# =====================================================

# Crosstab
heatmap_data = pd.crosstab(
    df['Assignments_Stress'],
    df['Use_Online_Communities_for_Support']
)

# Create figure
fig, ax = plt.subplots()

# Plot heatmap
im = ax.imshow(heatmap_data.values)

# Colorbar
plt.colorbar(im, ax=ax)

# Axis ticks and labels
ax.set_xticks(range(len(heatmap_data.columns)))
ax.set_xticklabels(heatmap_data.columns, rotation=45)

ax.set_yticks(range(len(heatmap_data.index)))
ax.set_yticklabels(heatmap_data.index)

# Add cell values
for i in range(len(heatmap_data.index)):
    for j in range(len(heatmap_data.columns)):
        ax.text(
            j, i,
            heatmap_data.iloc[i, j],
            ha="center",
            va="center"
        )

# Labels and title
ax.set_xlabel("Use Online Communities for Support")
ax.set_ylabel("Stress Level")
ax.set_title("Stress Level vs Use of Online Communities for Support")

# Show in Streamlit
st.pyplot(fig)

st.success("""
**Interpretation:**  
The biggest group is 18 students who have a stress level of 3 and only "Sometimes" 
use online communities for support. Another 16 students have a high stress level of 4 
and also use communities "Sometimes." It’s clear that "Sometimes" is the most popular 
choice for students feeling stress.
""")


# ----------- TAB 4: AINUN -----------

# ============ TAB 4: INDIVIDUAL VISUALIZATIONS ============
with tab4:
    st.subheader("Demographic Differences with Mental Health Experiences")
    st.write("""
    The purpose of this visualization is to identify and analyze demographic 
    differences in mental health experiences among students, focusing on how 
    gender, race and year of study influence student's perceptions and experience challenges.
    """)

    # ==================================================
    # SUMMARY METRIC BOXES
    # ==================================================

    TOTAL_RESPONDENTS = len(df)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Respondents", TOTAL_RESPONDENTS)

    with col2:
        majority_gender = filtered_data["Gender"].mode(dropna=True)[0] if not filtered_data.empty else "N/A"
        st.metric("Majority Gender", majority_gender)

    with col3:
        dominant_year = filtered_data["Year_of_Study"].mode(dropna=True)[0] if not filtered_data.empty else "N/A"
        st.metric("Dominant Year", dominant_year)

    ("📊 Summary Metrics")

    st.success("""
    **Summary:** The dataset is composed of 101 participants, which is an sample to see the significant trends in the mental health 
    of students and their internet use. The survey is dominated by female who form majority of the respondents meaning that the female 
    students are more represented in the survey. Regarding the level of study, Year 4 students are the majority group which implies that 
    final-year students are the most represented and can have different academic and mental health issues as compared to the lower years.
    """)

    
    left, right = st.columns(2)

    with left:
        ("1️⃣ Gender Distribution Across Year of Study")

        fig1 = px.histogram(
            filtered_data,
            x="Year_of_Study",
            color="Gender",
            barmode="group",
            labels={"Year_of_Study":"Year of Study","Number of Respondents":"Number of Respondents"}
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
            labels={"Social_Media_Positive_Impact_on_Wellbeing":"Perceived Positive Impact","Number of Respondents":"Number of Respondents"}
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
            labels={"Difficulty_Sleeping_University_Pressure":"Difficulty Sleeping","Number of Respondents":"Number of Respondents"}
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
            labels={"x":"Living Situation","y":"Year of Study","color":"Count"}
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
            labels={"Social_Media_Daily_Routine":"Social Media Routine","Number of Respondents":"Number of Respondents"}
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
        # SUMMARY
        # ==================================================

        st.success("""
        **Observation:** 

        The visualizations show clear demographic differences in student's mental health experiences. Female students report greater 
        effects from academic pressure and social media while higher-year students like to live more independently off-campus.
        Most respondents are full-time students, showing that academic demands are a key factor influencing student wellbeing.
        """)

   
# --- FOOTER ---
st.markdown("---")
st.caption("© 2025 Exploring Internet Use and Suicidality in Mental Health Populations | Designed with ❤️ using Streamlit & Plotly")
