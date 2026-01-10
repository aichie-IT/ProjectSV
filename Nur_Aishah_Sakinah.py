import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

px.defaults.template = "plotly_white"
px.defaults.color_continuous_scale = px.colors.sequential.Teal

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



# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Internet Use and Mental Health Dashboard",
    page_icon="🧠",
    layout="wide"
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

# ====== SIDEBAR ======
with st.sidebar:
    st.markdown(
    """
    <style>
    /* Card-like filter boxes */
    .stMultiSelect, .stSlider {
        background-color: #ffffff !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 10px !important;
        padding: 8px 10px !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    }

    /* Selected filter tags (stronger override) */
    div[data-baseweb="tag"] > div {
        background-color: #6c757d !important; /* modern gray tone */
        color: white !important;
        border-radius: 8px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.15);
    }

    /* Text inside tag */
    div[data-baseweb="tag"] span {
        color: white !important;
        font-weight: 500 !important;
    }

    /* Close (x) icon inside tag */
    div[data-baseweb="tag"] svg {
        fill: white !important;
        opacity: 0.9;
    }

    /* Slider color styling */
    .stSlider > div > div > div[data-testid="stThumbValue"] {
        color: #0073e6 !important;
        font-weight: bold !important;
    }
    .stSlider > div > div > div[data-testid="stTickBar"] {
        background: linear-gradient(to right, #0073e6, #00b894) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
        
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
            file_name="motor_accident_data.csv",
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

st.header("🧠 Internet Use & Mental Health Insights")
st.markdown("Analyzing interrelationships between social media usage, academic stress, and student wellbeing.")

# Summary box
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Students", f"{len(filtered_df):,}", border=True)
col2.metric("Avg. Age", f"{filtered_df['Age'].mean():.1f}", border=True)
col3.metric("Avg Stress Index", f"{filtered_numeric['Academic_Stress_Index'].mean():.2f}", border=True)
col4.metric("High Usage (%)", f"{(filtered_df['Social_Media_Use_Frequency'].isin(['5 to 6 hours per day','More than 6 hours per day']).mean()*100):.1f}%", border=True)

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
tab1, tab2, tab3, tab4 = st.tabs(["📉 Usage Patterns", "🎓 Academic Impact", "📈 Wellbeing Analysis", "🗺️ Correlation & Advanced Insights"])
    
# ============ TAB 1: USAGE PATTERNS ============
with tab1:
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
    st.markdown("### Real-Time Usage Summary")

    st.info(
        usage_summary(
            len(filtered_df),
            filtered_numeric["Social_Media_Hours_Numeric"].median(),
            (filtered_df["Social_Media_Use_Frequency"]
             .isin(["5 to 6 hours per day", "More than 6 hours per day"])
             .mean() * 100),
            filtered_numeric["Study_Hours_Numeric"].mean()
        )
    )

    st.markdown("---")
        
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
        filtered_df["Social_Media_Use_Frequency"].value_counts().reindex(freq_order),
        title="Distribution of Daily Social Media Usage",
        labels={"value": "Number of Students", "index": "Hours per Day"},
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig.update_layout(xaxis_tickangle=-30)
        
    usage_counts = filtered_df["Social_Media_Use_Frequency"].value_counts()
    total_students = usage_counts.sum()
    high_usage_pct = (
        filtered_df["Social_Media_Use_Frequency"]
        .isin(["5 to 6 hours per day", "More than 6 hours per day"])
        .mean() * 100
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info(
        f"Among the selected respondents (n = {total_students}), "
        f"{high_usage_pct:.1f}% report high social media usage of five hours or more per day. "
        f"This indicates that prolonged internet engagement is common and forms an important "
        f"context for analysing its relationship with academic stress and mental wellbeing."
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

    st.info(
        f"The most common usage category among the selected respondents is "
        f"'{dominant_group}', indicating that this level of internet engagement "
        f"represents the dominant behavioural pattern under the current filter selection."
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
       
    st.markdown("#### 💬 Observation")
    st.info(
        "Overall patterns observed in this section suggest that internet usage behaviour "
        "varies across student groups and is meaningfully associated with academic and "
        "wellbeing indicators. These observations motivate further correlation and "
        "multivariate analysis in subsequent sections."
    )
    
    
# ============ TAB 2: ACADEMIC IMPACT ============
with tab2:
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

    st.info(
        f"The visualization shows variations in academic stress across different levels "
        f"of social media usage. The average stress index across usage groups is "
        f"{mean_stress:.2f}, suggesting that increased internet exposure may be associated "
        f"with elevated academic stress, although the pattern is not uniform across all groups."
    )

        
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
    sleep_pct = (
        filtered_numeric["Sleep_Affected_By_Social_Media_Numeric"] >= 4
    ).mean() * 100

    st.info(
        f"Approximately {sleep_pct:.1f}% of students agree or strongly agree that "
        f"social media negatively affects their sleep. This highlights sleep disturbance "
        f"as a key wellbeing concern linked to prolonged internet use."
    )

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
    corr_val = safe_corr(
        filtered_numeric,
        "Social_Media_Hours_Numeric",
        "Assignments_Stress_Numeric"
    )

    if corr_val is not None:
        strength = (
            "weak" if abs(corr_val) < 0.3 else
            "moderate" if abs(corr_val) < 0.6 else
            "strong"
        )

        st.info(
            f"A {strength} positive correlation (r = {corr_val:.2f}) is observed between "
            f"daily social media usage and academic stress. This suggests an association "
            f"between increased online engagement and higher stress levels, though the "
            f"relationship does not imply direct causation."
        )
    else:
        st.info("Insufficient data to compute correlation under current filters.")

    # --- Observation Section (Fixed Indentation) ---
    st.markdown("#### 💬 Observation")
    st.success("""
    The majority of accidents are classified as minor. Helmet usage is generally high,
    which correlates with lower accident severity. Riders with valid licenses also
    exhibit safer driving trends, suggesting that training and enforcement play key roles.
    """)

# ============ TAB 3: WELLBEING ANALYSIS ============
with tab3:
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
    sleep_pct = (
        filtered_numeric["Sleep_Affected_By_Social_Media_Numeric"] >= 4
    ).mean() * 100

    st.info(
        f"Approximately {sleep_pct:.1f}% of students agree or strongly agree that "
        f"social media negatively affects their sleep. This highlights sleep disturbance "
        f"as a key wellbeing concern linked to prolonged internet use."
    )

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

    sleep_pct = (
        filtered_numeric["Sleep_Affected_By_Social_Media_Numeric"] >= 4
    ).mean() * 100

    st.info(
        f"Approximately {sleep_pct:.1f}% of students agree or strongly agree that "
        f"social media negatively affects their sleep. This highlights sleep disturbance "
        f"as a key wellbeing concern linked to prolonged internet use."
    )

       
    # --- Observation Section (Fixed Indentation) ---
    st.markdown("#### 💬 Observation")
    st.success("""
    The majority of accidents are classified as minor. Helmet usage is generally high,
    which correlates with lower accident severity. Riders with valid licenses also
    exhibit safer driving trends, suggesting that training and enforcement play key roles.
    """)

# ============ TAB 4: CORRELATION & INSIGHTS ============
with tab4:
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
    corr_val = safe_corr(
        filtered_numeric,
        "Social_Media_Hours_Numeric",
        "Assignments_Stress_Numeric"
    )

    if corr_val is not None:
        strength = (
            "weak" if abs(corr_val) < 0.3 else
            "moderate" if abs(corr_val) < 0.6 else
            "strong"
        )

        st.info(
            f"A {strength} positive correlation (r = {corr_val:.2f}) is observed between "
            f"daily social media usage and academic stress. This suggests an association "
            f"between increased online engagement and higher stress levels, though the "
            f"relationship does not imply direct causation."
        )
    else:
        st.info("Insufficient data to compute correlation under current filters.")

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

# --- FOOTER ---
st.markdown("---")
st.caption("© 2025 Motorbike Accident Dashboard | Designed with ❤️ using Streamlit & Plotly")
