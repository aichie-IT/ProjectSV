import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# --- MAIN TITLE ---
st.title(" Student Mental Health Monitoring Insights Dashboard")
st.markdown("Exploring the Relationship Between Internet Use and Mental Health.")

st.markdown("---")

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
st.header("📊 Overall Social Media Usage (All Respondents)")

# ------ DATASET OVERVIEW ------
st.subheader("📋 Dataset Overview")

st.markdown("""
This section provides an **overall overview of the survey dataset** collected from UMK students.
It allows users to understand the **structure, size, and completeness** of the data before any
filtering or visualization is applied.
""")

st.markdown("---")

# --- Dataset Preview ---
with st.expander("🔍 View Dataset Preview"):
    st.dataframe(df.head(20), use_container_width=True)

st.markdown("---")
# --- SUMMARY BOX ---
col1, col2, col3, col4 = st.columns(4)

top_academic = filtered_df['General_Academic_Performance'].mode()[0]
top_media = filtered_df['Social_Media_Use_Frequency'].mode()[0]

if not filtered_df.empty:
    col1.metric("Total Records", f"{len(df):,}", help="PLO 1: Total Respondent Records of Student", border=True)
    col2.metric("Avg. Age", f"{df['Age'].mean():.1f} years", help="PLO 2: Students Age", border=True)
    col3.metric("Academic Performance", top_academic, , help="PLO 2: Students Academic Performance", border=True)
    col4.metric("Social Media Usage", top_media, , help="PLO 2: Social Media Use Frecuency", border=True)
else:
    col1.metric("Total Records", "0", help="No data available")
    col2.metric("Avg. Age", "N/A", help="No data available")
    col3.metric("Academic Performance", "N/A", help="No data available")
    col4.metric("Social Media Usage", "N/A", help="No data available")

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

# Likert mapping
likert_map = {
    "Strongly Disagree": 1,
    "Disagree": 2,
    "Neutral": 3,
    "Agree": 4,
    "Strongly Agree": 5
}

# Numeric Likert Columns
for col in LIKERT_COLS:
    if col in df_numeric.columns:
        df_numeric[col + "_Numeric"] = (
            df_numeric[col]
            .astype(str)
            .str.split(" / ").str[0]
            .str.strip()
            .replace("nan", None)
            .map(likert_map)
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

mental_cols = [
    "Assignments_Stress",
    "Academic_Workload_Anxiety",
    "Difficulty_Sleeping_University_Pressure",
    "Sleep_Affected_By_Social_Media",
    "Studies_Affected_By_Social_Media"
]

# Likert (1–5)
for col in mental_cols:
    if col in df_numeric.columns:
        df_numeric[col + "_Numeric"] = (
            df_numeric[col]
            .astype(str)
            .str.split(" / ").str[0]
            .map(likert_map)
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

Help me fix this summary box, which is academic stress index show nan output


# ============ TAB 1: INTERNET USE VS. MENTAL HEALTH ============
with tab1:
    st.subheader("Internet Use & Mental Health Insights")
    st.markdown("Analyzing interrelationships between social media usage, academic stress, and student wellbeing.")

    # Summary box
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Students", f"{len(filtered_df):,}", border=True)
    col2.metric("Avg. Age", f"{filtered_df['Age'].mean():.1f}", border=True)
    col3.metric("Avg Stress Index", f"{filtered_numeric['Academic_Stress_Index'].mean():.2f}", border=True)
    col4.metric("High Usage (%)", f"{(filtered_df['Social_Media_Use_Frequency'].isin(['5 to 6 hours per day','More than 6 hours per day']).mean()*100):.1f}%", border=True)

    # Scientific Summary
    st.markdown("### Summary")
    st.info("""
    This overview highlights general distributions in the dataset. Most riders wear helmets, 
    and the average biking speed is moderate compared to the speed limits observed. 
    The distribution of accident severity suggests that minor and moderate accidents dominate, 
    implying that protective behaviors like helmet use and valid licensing may contribute 
    to reducing severe outcomes. These insights establish a foundation for understanding 
    how individual safety practices and environmental conditions interact.
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

        # Summary box
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Students", f"{len(filtered_df):,}", border=True)
        col2.metric("Avg. Age", f"{filtered_df['Age'].mean():.1f}", border=True)
        col3.metric("Most Common Social Media Usage", filtered_df['Social_Media_Use_Frequency'].mode()[0], border=True)
        col4.metric("Avg. Study Hours / Week", f"{filtered_numeric['Study_Hours_Numeric'].mean():.1f}", border=True)
        
        # Scientific Summary
        st.markdown("### Summary")
        st.info("""
        This overview highlights general distributions in the dataset. Most riders wear helmets, 
        and the average biking speed is moderate compared to the speed limits observed. 
        The distribution of accident severity suggests that minor and moderate accidents dominate, 
        implying that protective behaviors like helmet use and valid licensing may contribute 
        to reducing severe outcomes. These insights establish a foundation for understanding 
        how individual safety practices and environmental conditions interact.
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
        col1.metric("Study Impact Reported (%)", f"{(filtered_df['Studies_Affected_By_Social_Media'].map(likert_map).mean()/5*100):.1f}%", border=True)
        col2.metric("Avg. Academic Performance", f"{filtered_numeric['General_Academic_Performance_Numeric'].mean():.2f}", border=True)
        high_users = filtered_df['Social_Media_Use_Frequency'].isin(['5 to 6 hours per day', 'More than 6 hours per day']).mean() * 100
        col3.metric("High Social Media Users (%)", f"{high_users:.1f}%", border=True)
        col4.metric("Avg. Weekly Study Hours", f"{filtered_numeric['Study_Hours_Numeric'].mean():.1f}", border=True)

        # Scientific Summary
        st.markdown("### Summary")
        st.info("""
        This overview highlights general distributions in the dataset. Most riders wear helmets, 
        and the average biking speed is moderate compared to the speed limits observed. 
        The distribution of accident severity suggests that minor and moderate accidents dominate, 
        implying that protective behaviors like helmet use and valid licensing may contribute 
        to reducing severe outcomes. These insights establish a foundation for understanding 
        how individual safety practices and environmental conditions interact.
        """)
        st.markdown("---")

        col1, col2, col3 = st.columns(3)

        # Bar Chart
        filtered_numeric = filtered_numeric.dropna(
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
        col1.metric("Avg. Stress Level", f"{filtered_numeric['Assignments_Stress_Numeric'].mean():.2f}", border=True)
        col2.metric("Sleep Affected (%)", f"{(filtered_numeric['Sleep_Affected_By_Social_Media_Numeric'].mean()/5*100):.1f}%", border=True)
        col3.metric("Emotional Attachment", f"{filtered_numeric['Emotional_Connection_Social_Media_Numeric'].mean():.2f}", border=True)
        col4.metric("Online Help Seeking (%)", f"{(filtered_numeric['Seek_Help_Online_When_Stress_Numeric'].mean()/5*100):.1f}%", border=True)

        # Scientific Summary
        st.markdown("### Summary")
        st.info("""
        This overview highlights general distributions in the dataset. Most riders wear helmets, 
        and the average biking speed is moderate compared to the speed limits observed. 
        The distribution of accident severity suggests that minor and moderate accidents dominate, 
        implying that protective behaviors like helmet use and valid licensing may contribute 
        to reducing severe outcomes. These insights establish a foundation for understanding 
        how individual safety practices and environmental conditions interact.
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
        col1.metric("SM Hours ↔ Stress", f"{filtered_numeric[['Social_Media_Hours_Numeric', 'Assignments_Stress_Numeric']].corr().iloc[0,1]:.2f}", border=True)
        col2.metric("Study Hours ↔ Stress", f"{filtered_numeric[['Study_Hours_Numeric','Assignments_Stress_Numeric']].corr().iloc[0,1]:.2f}", border=True)
        impact_gap = (
            filtered_numeric['Social_Media_Positive_Impact_on_Wellbeing_Numeric'].mean(skipna=True)
            -
            filtered_numeric['Social_Media_Negative_Impact_on_Wellbeing_Numeric'].mean(skipna=True)
        )
        col3.metric("Wellbeing Impact Gap", f"{impact_gap:.2f}", border=True)
        col4.metric("Support-Seeking Score", f"{filtered_df['Use_Online_Communities_for_Support'].map(likert_map).mean():.2f}", border=True)
        # Scientific Summary
        st.markdown("### Summary")
        st.info("""
        This overview highlights general distributions in the dataset. Most riders wear helmets, 
        and the average biking speed is moderate compared to the speed limits observed. 
        The distribution of accident severity suggests that minor and moderate accidents dominate, 
        implying that protective behaviors like helmet use and valid licensing may contribute 
        to reducing severe outcomes. These insights establish a foundation for understanding 
        how individual safety practices and environmental conditions interact.
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
# ============ TAB 4: ADVANCED VISUALIZATIONS ============
with tab4:
    st.subheader("Distribution of Numeric Variables")
   
# --- FOOTER ---
st.markdown("---")
st.caption("© 2025 Motorbike Accident Dashboard | Designed with ❤️ using Streamlit & Plotly")
