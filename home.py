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
df["Social_Media_Use_Frequency"] = pd.Categorical(
    df["Social_Media_Use_Frequency"],
    categories=[
        "Less than 1 hour per day",
        "1 to 2 hours per day",
        "3 to 4 hours per day",
        "5 to 6 hours per day",
        "More than 6 hours per day"
    ],
    ordered=True
)

# ----------- ILYA -----------
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

# Mapping Impact
impact_map = {1: 'Positive Impact', 0: 'Negative Impact', 2: 'No impact'}
df['Social_Media_Positive_Impact_on_Wellbeing_Num'] = df['Social_Media_Positive_Impact_on_Wellbeing'].map({
    'Positive impact': 1, 'Negative impact': 0, 'No impact': 2
}).fillna(2)

# Mapping Race
race_map = {0: 'Malay', 1: 'Chinese', 2: 'Indian', 3: 'Other'}
df['Race_Num'] = df['Race'].map({'Malay': 0, 'Chinese': 1, 'Indian': 2, 'Others': 3, 'Other': 3}).fillna(3)

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
tab1, tab2, tab3, tab4 = st.tabs(["📊 Internet Use vs. Mental Health", "Ilya", "Hanis", "Ainun"])

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
    st.markdown("### Summary")
    st.info("""
    A total of **27 students** were analysed, with an average age of **22.7 years**, reflecting
    a typical undergraduate population.

    The **average Academic Stress Index of 2.98** shows a moderate level of academic-related
    stress, suggesting that many students experience noticeable pressure from coursework,
    assignments, and academic workload.

    While, **74.1% of students fall into the high social media usage category**
    (5 hours or more per day), highlighting the strong integration of social media into
    students’ daily routines. This high internet usage provides a critical context for examining its potential influence on academic stress and mental
    well-being.
    """)
    st.markdown("---")

    # --- TAB LAYOUT ---
    usage_tab, academic_tab, wellbeing_tab, insight_tab = st.tabs(["📉 Usage Patterns", "🎓 Academic Impact", "📈 Wellbeing Analysis", "🗺️ Correlation & Advanced Insights"])
    
    # ============ TAB 1.1: USAGE PATTERNS ============
    with usage_tab:
        st.subheader("Internet & Social Media Usage Patterns")
        st.markdown("Understand how much and how often students use the internet/social media.")

        # Summary box
        col1, col2, col3, col4 = st.columns(4)
        median_usage = filtered_numeric["Social_Media_Hours_Numeric"].median()
        high_usage_pct = (filtered_df["Social_Media_Use_Frequency"].isin(["5 to 6 hours per day", "More than 6 hours per day"]).mean() * 100)
        avg_study_hours = filtered_numeric["Study_Hours_Numeric"].mean()
        time_waste_pct = (filtered_df["Social_Media_Waste_Time"].isin(["Agree", "Strongly Agree"]).mean() * 100)

        col1.metric("Median Social Media Hours/Day", f"{median_usage:.1f} hrs", help="Typical daily social media usage (median)", border=True)
        col2.metric("High Usage Group (%)", f"{high_usage_pct:.1f}%", help="Students using ≥5 hours/day", border=True)
        col3.metric("Avg. Study Hours/Week", f"{avg_study_hours:.1f}", help="Average academic study commitment", border=True)
        col4.metric("Perceived Time Loss (%)", f"{time_waste_pct:.1f}%", help="Students who feel social media wastes their time", border=True)
        
        # Scientific Summary
        st.markdown("### Summary")
        st.info("""
        The **median social media usage of 7 hours per day** shows that social
        media is heavily embedded in students’ daily routines, with usage skewed
        towards prolonged usage.

        Approximately **74.1% of students belong to the high-usage group**
        (5 hours or more per day), confirming that excessive internet exposure is
        common within the sample. In contrast, the **average study time is 6.2 hours
        per week**, suggesting a relatively lower allocation of time to academic
        activities.

        In fact, **none of the students explicitly perceived social media as a
        waste of time (0.0%)**, which may reflect normalisation of high usage or a lack
        of awareness of its potential impact on productivity rather than an absence
        of actual time displacement.
        """)
        st.markdown("---")

        col1, col2, col3, col4 = st.columns(4)
        
        # Bar Chart
        freq_order = [
            "Less than 1 hour per day",
            "1 to 2 hours per day",
            "3 to 4 hours per day",
            "5 to 6 hours per day",
            "More than 6 hours per day"
        ]

        filtered_df["Social_Media_Use_Frequency"] = pd.Categorical(
            filtered_df["Social_Media_Use_Frequency"],
            categories=freq_order,
            ordered=True
        )

        fig = px.bar(
            filtered_df,
            x="Social_Media_Use_Frequency",
            title="Distribution of Daily Social Media Usage",
            labels={"Social_Media_Use_Frequency": "Hours per Day"},
            color_discrete_sequence=px.colors.qualitative.Set2
        )

        st.plotly_chart(fig, use_container_width=True)
        st.success("""
        **Interpretation:** Most students show moderate-to-high social media usage, indicating its strong integration into daily routines.
        """)
            
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
        st.success("""
        **Interpretation:** Most students show moderate-to-high social media usage, indicating its strong integration into daily routines.
        """)

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
        st.success("""
        **Interpretation:** Most students show moderate-to-high social media usage, indicating its strong integration into daily routines.
        """)

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
        st.success("""
        **Interpretation:** Most students show moderate-to-high social media usage, indicating its strong integration into daily routines.
        """)

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

        st.success("""
        **Interpretation:** Most students show moderate-to-high social media usage, indicating its strong integration into daily routines.
        """)
       
        # --- Observation Section (Fixed Indentation) ---
        st.markdown("#### 💬 Observation")
        st.success("""
        The majority of accidents are classified as minor. Helmet usage is generally high,
        which correlates with lower accident severity. Riders with valid licenses also
        exhibit safer driving trends, suggesting that training and enforcement play key roles.
        """)
    
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

        col1.metric("Study Impact (%)", f"{(study_impact.mean()/5*100):.1f}%" if not study_impact.empty else "N/A", help="Average perceived impact of social media on studies", border=True)
        col2.metric("Avg. Academic Performance", f"{academic_perf.mean():.2f}" if not academic_perf.empty else "N/A", help="Numeric scale: 1=Below Avg → 4=Excellent", border=True)
        col3.metric("High Usage Students (%)", f"{high_users_pct:.1f}%", help="Students using ≥5 hours/day", border=True)
        col4.metric("Avg. Weekly Study Hours", f"{study_hours.mean():.1f}" if not study_hours.empty else "N/A", help="Self-reported weekly study time", border=True)
        
        # Scientific Summary
        st.markdown("### Summary")
        st.info("""
        The results show that social media has a noticeable influence on students’ academic activities. 
        Approximately **{(study_impact.mean()/5*100):.1f}%** of students reported that their studies are affected by social media usage, 
        showing that online engagement may interfere with academic focus and productivity.

        The **average academic performance score of {academic_perf.mean():.2f}** suggests that students generally maintain 
        moderate academic achievement despite high levels of social media use. Notably, **{high_users_pct:.1f}%** of students 
        are classified as high social media users, spending at least five hours per day on these platforms.

        In addition, students reported an **average weekly study time of {study_hours.mean():.1f} hours**, 
        which may help explain the perceived academic impact when combined with heavy social media usage.
        """)
        st.markdown("---")

        col1, col2, col3 = st.columns(3)

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
        st.success("""
        **Interpretation:** Most students show moderate-to-high social media usage, indicating its strong integration into daily routines.
        """)
        
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
        st.success("""
        **Interpretation:** Most students show moderate-to-high social media usage, indicating its strong integration into daily routines.
        """)

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
        st.success("""
        **Interpretation:** Most students show moderate-to-high social media usage, indicating its strong integration into daily routines.
        """)

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
        st.success("""
        **Interpretation:** Most students show moderate-to-high social media usage, indicating its strong integration into daily routines.
        """)
        # --- Observation Section (Fixed Indentation) ---
        st.markdown("#### 💬 Observation")
        st.success("""
        The majority of accidents are classified as minor. Helmet usage is generally high,
        which correlates with lower accident severity. Riders with valid licenses also
        exhibit safer driving trends, suggesting that training and enforcement play key roles.
        """)

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

        col1.metric("Avg. Stress Level", f"{stress.mean():.2f}" if not stress.empty else "N/A", border=True)
        col2.metric("Sleep Affected (%)", f"{(sleep.mean()/5*100):.1f}%" if not sleep.empty else "N/A", border=True)
        col3.metric("Emotional Attachment", f"{emotion.mean():.2f}" if not emotion.empty else "N/A", border=True)
        col4.metric("Online Help Seeking (%)", f"{(help_seek.mean()/5*100):.1f}%" if not help_seek.empty else "N/A", border=True)

        # Scientific Summary
        st.markdown("### Summary")
        st.info("""
        The wellbeing analysis indicates a **moderate average stress level of {stress.mean():.2f}**, 
        suggesting that academic and online demands contribute noticeably to students’ daily stress.

        Approximately **{(sleep.mean()/5*100):.1f}%** of students reported that their sleep patterns are affected by social media use, 
        highlighting the potential impact of excessive screen time on rest and recovery. 
        The **emotional attachment score of {emotion.mean():.2f}** reflects a moderate emotional connection to social media platforms.

        Furthermore, **{(help_seek.mean()/5*100):.1f}%** of students indicated that they seek help or emotional support online during stressful periods, 
        suggesting that digital platforms play a significant role in students’ coping and support-seeking behaviours.
        """)
        st.markdown("---")

        col1, col2 = st.columns(2)

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
        st.success("""
        **Interpretation:** Most students show moderate-to-high social media usage, indicating its strong integration into daily routines.
        """)

        # Parallel coordinates
        parallel_df = df_numeric[
            [
                'Social_Media_Use_Frequency',
                'Assignments_Stress',
                'Academic_Workload_Anxiety',
                'Sleep_Affected_By_Social_Media',
                'Studies_Affected_By_Social_Media'
            ]
        ].dropna()

        fig = px.parallel_coordinates(
            parallel_df,
            dimensions=[
                'Assignments_Stress',
                'Academic_Workload_Anxiety',
                'Sleep_Affected_By_Social_Media',
                'Studies_Affected_By_Social_Media'
            ],
            color='Assignments_Stress',
            color_continuous_scale=CONTINUOUS_SCALE
        )
        fig.update_layout(template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

        st.success("""
        **Interpretation:** Most students show moderate-to-high social media usage, indicating its strong integration into daily routines.
        """)
       
        # --- Observation Section (Fixed Indentation) ---
        st.markdown("#### 💬 Observation")
        st.success("""
        The majority of accidents are classified as minor. Helmet usage is generally high,
        which correlates with lower accident severity. Riders with valid licenses also
        exhibit safer driving trends, suggesting that training and enforcement play key roles.
        """)

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
        st.markdown("### Summary")
        st.info("""
        The correlation analysis shows a **weak positive relationship (r = {corr_sm_stress:.2f})** between daily social media usage and academic stress, 
        showing that increased time spent online is associated with slightly higher stress levels.

        Similarly, **study hours exhibit a weak positive correlation with stress (r = {corr_study_stress:.2f})**, 
        suggesting that higher academic workload may contribute to increased stress rather than reducing it.

        The **wellbeing impact gap of {impact_gap:.2f}** indicates that perceived positive effects of social media slightly outweigh negative effects, 
        implying a balanced but cautious role of social media in students’ wellbeing.

        Lastly, the **support-seeking score of {support_score.mean():.2f}** reflects a moderate tendency for students to use online communities 
        as a source of emotional or mental health support during stressful periods.
        """)
        st.markdown("---")

        col1, col2 = st.columns(2)

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
        st.error("""
        Strong correlations highlight the need for institutional awareness and early intervention.
        """)

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
         
       
        # --- Observation Section (Fixed Indentation) ---
        st.markdown("#### 💬 Observation")
        st.success("""
        The majority of accidents are classified as minor. Helmet usage is generally high,
        which correlates with lower accident severity. Riders with valid licenses also
        exhibit safer driving trends, suggesting that training and enforcement play key roles.
        """)

# ----------- ILYA -----------

# ============ TAB 2: ACCIDENT FACTORS ============
with tab2:
    st.subheader("Accident Severity by Categorical Factors")

# ----------- HANIS NABILA -----------
# ============ TAB 3: NUMERICAL ANALYSIS ============
with tab3:
    st.subheader("Distribution of Numeric Variables")
    


# ----------- AINUN -----------
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

st.subheader("📊 Summary Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Respondents", TOTAL_RESPONDENTS)

with col2:
    majority_gender = filtered_data["Gender"].mode(dropna=True)[0] if not filtered_data.empty else "N/A"
    st.metric("Majority Gender", majority_gender)

with col3:
    dominant_year = filtered_data["Year_of_Study"].mode(dropna=True)[0] if not filtered_data.empty else "N/A"
    st.metric("Dominant Year", dominant_year)

with col4:
    dominant_social_media = (
        filtered_data["Social_Media_Daily_Routine"].mode(dropna=True)[0]
        if not filtered_data.empty else "N/A"
    )
    st.metric("Common Social Media Routine", dominant_social_media)
    
left, right = st.columns(2)

with left:
    1️⃣ Gender Distribution Across Year of Study**

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

    st.subheader("2️⃣ Gender vs Social Media Impact")

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

    st.subheader("3️⃣ Gender vs Difficulty Sleeping")

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
     
    st.success("""
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
        labels={"Social_Media_Daily_Routine":"Social Media Routine","Number of Respondents":"Number of Respondents"}
    )
    st.plotly_chart(fig5, use_container_width=True)
    
    st.success("""
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
