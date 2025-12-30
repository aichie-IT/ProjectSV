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

# --- PAGE CONFIG ---
st.set_page_config(page_title="Internet Use and Mental Health Dashboard", page_icon="🧠", layout="wide")


# --- LOAD DATA ---
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/aichie-IT/ProjectSV/refs/heads/main/exploring_internet_use.csv"
    df = pd.read_csv(url)
    return df

df = load_data(https://docs.google.com/spreadsheets/d/e/2PACX-1vQnrGG72xRS-qLoiM2zon4eP8t5XMiO5MhoLUEe2jJer0G5EzodiU4e0NOmx_ssmCwZf-AnbQXhBbTM/pub?gid=1791189796&single=true&output=csv)\

# Fix encoding issues
df = df.replace({"â\x80\x93": "-", "–": "-", "—": "-"}, regex=True)

# Standardize ranges
for col in ["Social_Media_Use_Frequency", "Hours_Study_per_Week"]:
    df[col] = df[col].astype(str).str.replace("-", " to ", regex=False).str.strip()
    
# Categorical ordering
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

# Numeric transformations
likert_map = {
    "Strongly Disagree": 1,
    "Disagree": 2,
    "Neutral": 3,
    "Agree": 4,
    "Strongly Agree": 5
}

mental_cols = [
    'Assignments_Stress',
    'Academic_Workload_Anxiety',
    'Difficulty_Sleeping_University_Pressure',
    'Sleep_Affected_By_Social_Media',
    'Studies_Affected_By_Social_Media'
]

df_numeric = df.copy()

for col in mental_cols:
    df_numeric[col] = (
        df_numeric[col]
        .astype(str)
        .str.split(" / ").str[0]
        .map(likert_map)
    )

df_numeric["Academic_Stress_Index"] = df_numeric[mental_cols[:3]].mean(axis=1)

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
    st.info(f"**Total Records:** {len(df):,}\n\n**Columns:** {len(df.columns)}")

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


st.header(" Student Mental Health Monitoring Insights Dashboard")
st.markdown("Exploring the Relationship Between Internet Use and Mental Health.")

st.markdown("---")

# --- SUMMARY BOX ---
col1, col2, col3, col4 = st.columns(4)

if not filtered_df.empty:
    col1.metric("Total Records", f"{len(filtered_df):,}", help="PLO 1: Total Respondent Records of Student", border=True)
    col2.metric("Avg. Age", f"{filtered_df['Age'].mean():.1f} years", help="PLO 2: Students Age", border=True)
    col3.metric("Avg. Positive Impact", f"{filtered_df['Social_Media_Positive_Impact_on_Wellbeing'].mean():.1f}", help="PLO 3: Positive Impact on Wellbeing", border=True)
    col4.metric("Avg. Negative Impact", f"{filtered_df['Social_Media_Negative_Impact_on_Wellbeing'].mean():.1f}", help="PLO 4: Negative Impact on Wellbeing", border=True)
else:
    col1.metric("Total Records", "0", help="No data available")
    col2.metric("Avg. Age", "N/A", help="No data available")
    col3.metric("Avg. Positive Impact", "N/A", help="No data available")
    col4.metric("Avg. Negative Impact", "N/A", help="No data available")

st.markdown("---")

# --- TAB LAYOUT ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Internet Use vs. Mental Health", "📈 Numerical Analysis", "📉 Advanced Visualizations", "🗺️ Correlation Insights"])

# ============ TAB 1: INTERNET USE VS. MENTAL HEALTH ============
with tab1:
    st.subheader("🧠 Internet Use & Mental Health Insights")
    st.markdown("Analyzing interrelationships between social media usage, academic stress, and student wellbeing.")

    # Summary box
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Students", f"{len(filtered_df):,}", border=True)
    col2.metric("Avg. Age", f"{filtered_df['Age'].mean():.1f}", border=True)
    col3.metric("Avg Stress Index", f"{df_numeric['Academic_Stress_Index'].mean():.2f}", border=True)
    col4.metric("High Usage (%)", f"{(df['Social_Media_Use_Frequency'].isin(['5 to 6 hours per day','More than 6 hours per day']).mean()*100):.1f}%", border=True)

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
    tab1, tab2, tab3, tab4 = st.tabs(["📉 Usage Patterns", "🎓 Academic Impact", "📈 Wellbeing Analysis", "🗺️ Correlation & Advanced Insights"])
    
    # ============ TAB 1.1: USAGE PATTERNS ============
    with tab1:
        st.subheader("Internet & Social Media Usage Patterns")
        st.markdown("Understand how much and how often students use the internet/social media.")

        # Summary box
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Students", f"{len(filtered_df):,}", border=True)
        col2.metric("Avg. Age", f"{filtered_df['Age'].mean():.1f}", border=True)
        col3.metric("Most Common Social Media Usage", filtered_df['Social_Media_Use_Frequency'].mode()[0], border=True)
        col4.metric("Avg. Study Hours / Week", f"{filtered_df['Study_Hours_Numeric'].mean():.1f}", border=True)
        
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
        with col1:
            freq_order = ["< 1 hr", "1–2 hrs", "3–4 hrs", "5–6 hrs", "> 6 hrs"]

            fig = px.bar(
                df["Social_Media_Use_Frequency"].value_counts().reindex(freq_order),
                title="Distribution of Daily Social Media Usage",
                labels={"value": "Number of Students", "index": "Hours per Day"},
                color_discrete_sequence=px.colors.qualitative.Set2
            )

            fig.update_layout(xaxis_tickangle=-30)
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
                df["Hours_Study_per_Week"].value_counts().reindex(study_order),
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
        with col2:
            fig = px.box(
                df,
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
        with col3:
            st.subheader("Perception of Wasting Time on Social Media")

            fig = px.histogram(
                df,
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
        with col4:
            resource_counts = df[
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
    with tab2:
        st.subheader("Academic Impact of Social Media Analysis")
        st.markdown("Examine whether internet usage affects academic outcomes.")

        # Summary box
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Study Impact Reported (%)", f"{(filtered_df['Studies_Affected_By_Social_Media'].map(likert_map).mean()/5*100):.1f}%", border=True)
        col2.metric("Avg. Academic Performance", f"{filtered_df['General_Academic_Performance'].mean():.2f}", border=True)
        high_users = filtered_df['Social_Media_Use_Frequency'].isin(['5–6 hrs', '> 6 hrs']).mean() * 100
        col3.metric("High Social Media Users (%)", f"{high_users:.1f}%", border=True)
        col4.metric("Avg. Weekly Study Hours", f"{filtered_df['Study_Hours_Numeric'].mean():.1f}", border=True)

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
        with col1:
            st.subheader("Academic Stress vs Social Media Usage")

            usage_group_mean = (
                df_numeric.groupby("Social_Media_Use_Frequency")
                ["Academic_Stress_Index"]
                .mean()
                .reset_index()
            )

            fig = px.bar(
                usage_group_mean,
                x="Social_Media_Use_Frequency",
                y="Academic_Stress_Index",
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
        with col2:
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
        with col3:
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
       

    # ============ TAB 1.3: WELLBEING ANALYSIS ============
    with tab3:
        st.subheader("Mental & Emotional Wellbeing")
        st.markdown("Understand stress, sleep, and emotional responses linked to online behaviour.")

        # Summary box
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Avg. Stress Level", f"{filtered_df['Assignments_Stress'].map(likert_map).mean():.2f}", border=True)
        col2.metric("Sleep Affected (%)", f"{(filtered_df['Sleep_Affected_By_Social_Media'].map(likert_map).mean()/5*100):.1f}%", border=True)
        col3.metric("Emotional Attachment", f"{filtered_df['Emotional_Connection_Social_Media'].map(likert_map).mean():.2f}", border=True)
        col4.metric("Online Help Seeking (%)", f"{(filtered_df['Seek_Help_Online_When_Stress'].map(likert_map).mean()/5*100):.1f}%", border=True)

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
        with col1:
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
        with col2:
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
    with tab4:
        st.subheader("Correlation & Deep Analysis")
        st.markdown("Reveal hidden relationships across variables (lecturer favourite).")

        # Summary box
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("SM Hours ↔ Stress", f"{filtered_df[['Social_Media_Hours_Numeric','Assignments_Stress']].corr().iloc[0,1]:.2f}", border=True)
        col2.metric("Study Hours ↔ Stress", f"{filtered_df[['Study_Hours_Numeric','Assignments_Stress']].corr().iloc[0,1]:.2f}", border=True)
        impact_gap = (
            filtered_df['Social_Media_Positive_Impact_on_Wellbeing'].map(likert_map).mean()
            -
            filtered_df['Social_Media_Negative_Impact_on_Wellbeing'].map(likert_map).mean())
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
        with col1:
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
        with col2:
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
