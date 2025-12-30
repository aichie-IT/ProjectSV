import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

px.defaults.template = "plotly_white"
px.defaults.color_continuous_scale = px.colors.sequential.Teal


# --- PAGE CONFIG ---
st.set_page_config(page_title="Internet Use and Mental Health Monitoring Insights Dashboard", page_icon="📈", layout="wide")


# --- LOAD DATA ---
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/aichie-IT/ProjectSV/refs/heads/main/exploring_internet_use.csv"
    df = pd.read_csv(url)
    return df

df = load_data(https://docs.google.com/spreadsheets/d/e/2PACX-1vQnrGG72xRS-qLoiM2zon4eP8t5XMiO5MhoLUEe2jJer0G5EzodiU4e0NOmx_ssmCwZf-AnbQXhBbTM/pub?gid=1791189796&single=true&output=csv)\

# Cleaning & preprocessing (AFTER load)
df = df.replace({
    "â\x80\x93": "-",
    "–": "-",
    "—": "-"
}, regex=True)

for col in ["Social_Media_Use_Frequency", "Hours_Study_per_Week"]:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace("-", " to ", regex=False)
        .str.strip()
    )

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

stress_cols = [
    'Assignments_Stress',
    'Academic_Workload_Anxiety',
    'Difficulty_Sleeping_University_Pressure'
]

df_numeric = df.copy()
for col in stress_cols:
    df_numeric[col] = (
        df_numeric[col]
        .astype(str)
        .str.split(" / ").str[0]
        .map(likert_map)
    )

df_numeric["Academic_Stress_Index"] = df_numeric[stress_cols].mean(axis=1)

# ====== SIDEBAR ======
with st.sidebar:
    st.title("Dashboard Controls")

    # --- Data Summary ---
    st.markdown("### 🧾 Data Summary")
    st.info(f"**Total Records:** {len(df):,}\n\n**Columns:** {len(df.columns)}")

    # --- Filters Section ---
    with st.expander("🎯 Filter Options", expanded=True):
        st.markdown("Select filters to refine your dashboard view:")

        # --- Multi-select Filters ---
        severity = st.multiselect(
            "Accident Severity",
            options=sorted(df["Accident_Severity"].dropna().unique()),
            default=sorted(df["Accident_Severity"].dropna().unique())
        )

        weather = st.multiselect(
            "Weather Condition",
            options=sorted(df["Weather"].dropna().unique()),
            default=sorted(df["Weather"].dropna().unique())
        )

        time_of_day = st.multiselect(
            "Time of Day",
            options=sorted(df["Time_of_Day"].dropna().unique()),
            default=sorted(df["Time_of_Day"].dropna().unique())
        )

        road_type = st.multiselect(
            "Road Type",
            options=sorted(df["Road_Type"].dropna().unique()),
            default=sorted(df["Road_Type"].dropna().unique())
        )

        # --- Optional Filters ---
        if "Biker_Alcohol" in df.columns:
            alcohol = st.multiselect(
                "Biker Alcohol Consumption",
                options=sorted(df["Biker_Alcohol"].dropna().unique()),
                default=sorted(df["Biker_Alcohol"].dropna().unique())
            )
        else:
            alcohol = []

        if "Traffic_Density" in df.columns:
            traffic = st.multiselect(
                "Traffic Density",
                options=sorted(df["Traffic_Density"].dropna().unique()),
                default=sorted(df["Traffic_Density"].dropna().unique())
            )
        else:
            traffic = []

        if "Valid_Driving_License" in df.columns:
            license_status = st.multiselect(
                "Valid Driving License",
                options=sorted(df["Valid_Driving_License"].dropna().unique()),
                default=sorted(df["Valid_Driving_License"].dropna().unique())
            )
        else:
            license_status = []

        # --- Numeric Filter: Biker Age ---
        if "Biker_Age" in df.columns:
            min_age, max_age = st.slider(
                "Filter by Biker Age",
                int(df["Biker_Age"].min()),
                int(df["Biker_Age"].max()),
                (int(df["Biker_Age"].min()), int(df["Biker_Age"].max()))
            )
        else:
            min_age, max_age = None, None

        # --- Apply Filters ---
        filtered_df = df.copy()

        if severity:
            filtered_df = filtered_df[filtered_df["Accident_Severity"].isin(severity)]
        if weather:
            filtered_df = filtered_df[filtered_df["Weather"].isin(weather)]
        if time_of_day:
            filtered_df = filtered_df[filtered_df["Time_of_Day"].isin(time_of_day)]
        if road_type:
            filtered_df = filtered_df[filtered_df["Road_Type"].isin(road_type)]
        if alcohol:
            filtered_df = filtered_df[filtered_df["Biker_Alcohol"].isin(alcohol)]
        if traffic:
            filtered_df = filtered_df[filtered_df["Traffic_Density"].isin(traffic)]
        if license_status:
            filtered_df = filtered_df[filtered_df["Valid_Driving_License"].isin(license_status)]
        if min_age is not None:
            filtered_df = filtered_df[
                (filtered_df["Biker_Age"] >= min_age) & (filtered_df["Biker_Age"] <= max_age)
            ]

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
color_theme = px.colors.qualitative.Pastel


# --- MAIN TITLE ---
st.title("🏍️ Motorbike Accident Insights Dashboard")
st.markdown("Explore accident patterns and biker behaviors with interactive visual analytics.")

st.markdown("---")

# --- SUMMARY BOX ---
col1, col2, col3, col4 = st.columns(4)

if not filtered_df.empty:
    col1.metric("Total Records", f"{len(filtered_df):,}", help="PLO 1: Total Motor Accident Records", border=True)
    col2.metric("Avg. Age", f"{filtered_df['Biker_Age'].mean():.1f} years", help="PLO 2: Average Biker Age", border=True)
    col3.metric("Avg. Speed", f"{filtered_df['Bike_Speed'].mean():.1f} km/h", help="PLO 3: Average Bike Speed", border=True)
    col4.metric("Avg. Travel Distance", f"{filtered_df['Daily_Travel_Distance'].mean():.1f} km", help="PLO 4: Average Daily Travel Distance", border=True)
else:
    col1.metric("Total Records", "0", help="No data available")
    col2.metric("Avg. Age", "N/A", help="No data available")
    col3.metric("Avg. Speed", "N/A", help="No data available")
    col4.metric("Avg. Travel Distance", "N/A", help="No data available")

st.markdown("---")

# --- TAB LAYOUT ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["⚙️ General Overview", "📊 Accident Factors", "📈 Numerical Analysis", "📉 Advanced Visualizations", "🗺️ Correlation Insights", "🏍️ Riding Behavior Insights"])

# ============ TAB 1: GENERAL OVERVIEW ============
with tab1:
    st.subheader("Distribution Overview")
    st.markdown("Overview of accident severity, helmet use, and license validity.")

    # Summary box
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Records", f"{len(filtered_df):,}", border=True)
    col2.metric("Avg. Age", f"{filtered_df['Biker_Age'].mean():.1f}", border=True)
    col3.metric("Avg. Speed", f"{filtered_df['Bike_Speed'].mean():.1f} km/h", border=True)
    col4.metric("Helmet Usage (%)", f"{(filtered_df['Wearing_Helmet'].value_counts(normalize=True).get('Yes',0)*100):.1f}%", border=True)

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

    # Pie: Accident Severity
    with col1:
        severity_counts = filtered_df["Accident_Severity"].value_counts().reset_index()
        severity_counts.columns = ["Accident_Severity", "Count"]
        fig1 = px.pie(
            severity_counts, 
            values="Count", 
            names="Accident_Severity",
            title="Accident Severity Distribution",
            color_discrete_sequence=color_theme
        )
        st.plotly_chart(fig1, use_container_width=True)
        st.success("""
        **Interpretation:** Most accidents are classified as *minor*, suggesting effective safety measures such as helmet usage and speed regulation.
        """)

    # Pie: Helmet Usage
    with col2:
        helmet_counts = filtered_df["Wearing_Helmet"].value_counts().reset_index()
        helmet_counts.columns = ["Wearing_Helmet", "Count"]
        fig2 = px.pie(
            helmet_counts, 
            values="Count", 
            names="Wearing_Helmet", 
            title="Wearing Helmet Distribution",
            color_discrete_sequence=color_theme
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.success("""
        **Interpretation:** Helmet usage exceeds 70%, which correlates with fewer severe accidents and lower injury rates.
        """)

    # Pie: Valid License
    with col3:
        license_counts = filtered_df["Valid_Driving_License"].value_counts().reset_index()
        license_counts.columns = ["Valid_Driving_License", "Count"]
        fig3 = px.pie(
            license_counts, 
            values="Count", 
            names="Valid_Driving_License",
            title="Valid Driving License Distribution",
            color_discrete_sequence=color_theme
        )
        st.plotly_chart(fig3, use_container_width=True)
        st.success("""
        **Interpretation:** Riders with valid licenses tend to experience less severe accidents, supporting the importance of formal riding training.
        """)
        
    # --- Observation Section (Fixed Indentation) ---
    st.markdown("#### 💬 Observation")
    st.success("""
    The majority of accidents are classified as minor. Helmet usage is generally high,
    which correlates with lower accident severity. Riders with valid licenses also
    exhibit safer driving trends, suggesting that training and enforcement play key roles.
    """)

# ============ TAB 2: ACCIDENT FACTORS ============
with tab2:
    st.subheader("Accident Severity by Categorical Factors")


# ============ TAB 3: NUMERICAL ANALYSIS ============
with tab3:
    st.subheader("Distribution of Numeric Variables")
    st.markdown("Analyze numeric relationships such as speed, age, experience, and travel distance.")

    col1, col2, col3 = st.columns(3)
    col1.metric("Avg. Bike Speed", f"{filtered_df['Bike_Speed'].mean():.1f} km/h", border=True)
    col2.metric("Avg. Daily Distance", f"{filtered_df['Daily_Travel_Distance'].mean():.1f} km", border=True)
    col3.metric("Avg. Riding Experience", f"{filtered_df['Riding_Experience'].mean():.1f} years", border=True)

    st.markdown("### Summary")
    st.info("""
    Numerical distributions reveal that most bikers are within the mid-age range with moderate experience. 
    Speed and daily distance vary widely, reflecting diverse riding habits. The data indicates that 
    excessive speed is a major contributor to higher accident severity, whereas more riding experience 
    correlates with fewer severe outcomes.
    """)
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        fig6 = px.histogram(
            filtered_df, x="Biker_Age", nbins=20,
            title="Distribution of Biker Age",
            color_discrete_sequence=color_theme
        )
        st.plotly_chart(fig6, use_container_width=True)
        st.success("""
        **Interpretation:** Most bikers are aged between 20–40, which corresponds to moderate accident severity, possibly due to higher riding activity.
        """)

        fig7 = px.histogram(
            filtered_df, x="Bike_Speed", nbins=20,
            title="Distribution of Bike Speed",
            color_discrete_sequence=color_theme
        )
        st.plotly_chart(fig7, use_container_width=True)
        st.warning("""
        **Interpretation:** Speed distribution skews toward 60–80 km/h, and riders above this range tend to experience more severe accidents.
        """)

    with col2:
        fig8 = px.histogram(
            filtered_df, x="Riding_Experience", nbins=20,
            title="Distribution of Riding Experience",
            color_discrete_sequence=color_theme
        )
        st.plotly_chart(fig8, use_container_width=True)
        st.info("""
        **Interpretation:** Greater riding experience is associated with fewer accidents, highlighting the protective role of skill and familiarity.
        """)

        fig9 = px.histogram(
            filtered_df, x="Daily_Travel_Distance", nbins=20,
            title="Distribution of Daily Travel Distance",
            color_discrete_sequence=color_theme
        )
        st.plotly_chart(fig9, use_container_width=True)
        st.success("""
        **Interpretation:** Moderate daily travel distances (10–30 km) dominate the dataset, while excessive distance relates to fatigue and higher risk.
        """)
    st.markdown("#### 💬 Observation")
    st.success("""
    Riders with greater experience tend to maintain safer speeds. The histogram peaks for moderate 
    speed and mid-age groups align with less severe accident rates, reinforcing the role of skill 
    and maturity in risk mitigation.
    """)

# ============ TAB 4: ADVANCED VISUALIZATIONS ============
with tab4:
    st.subheader("Advanced Statistical Visualizations")
    st.markdown("Explore deeper numerical relationships using box, violin, and scatter plots.")

    # Summary box
    corr_pair = df.corr(numeric_only=True).abs().unstack().sort_values(ascending=False)
    top_corr = corr_pair[corr_pair < 1].head(1)
    feature_a, feature_b = top_corr.index[0]
    value = top_corr.values[0]
    st.metric("Strongest Correlation", f"{feature_a} ↔ {feature_b}", f"{value:.2f}", border=True)

    st.markdown("### Summary")
    st.info("""
    These visualizations explore how accident severity interacts with continuous variables like age, 
    speed, and distance. Box and violin plots show clear separation in speed and experience across 
    severity levels. Scatter plots reveal positive relationships between higher bike speed and greater 
    accident severity, confirming that speed remains a dominant factor.
    """)
    st.markdown("---")
    
    sns.set_style("whitegrid")

    # Helper function
    def show_plot(title, xlabel, ylabel, rotation=False):
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        if rotation:
            plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(plt.gcf())
        plt.clf()

    # --- BOX PLOTS ---
    with st.expander("📦 Box Plots"):
        plt.figure(figsize=(12, 7))
        sns.boxplot(x='Accident_Severity', y='Biker_Age', data=filtered_df, palette='viridis')
        show_plot('Distribution of Biker Age by Accident Severity', 'Accident Severity', 'Biker Age')
        st.success("**Interpretation:** Younger bikers show higher accident severity, suggesting overconfidence and less risk awareness.")

        plt.figure(figsize=(12, 7))
        sns.boxplot(x='Accident_Severity', y='Riding_Experience', data=filtered_df, palette='viridis')
        show_plot('Distribution of Riding Experience by Accident Severity', 'Accident Severity', 'Riding Experience (Years)')
        st.success("**Interpretation:** Younger bikers show higher accident severity, suggesting overconfidence and less risk awareness.")

        plt.figure(figsize=(12, 7))
        sns.boxplot(x='Accident_Severity', y='Daily_Travel_Distance', data=filtered_df, palette='viridis')
        show_plot('Distribution of Daily Travel Distance by Accident Severity', 'Accident Severity', 'Daily Travel Distance')
        st.success("**Interpretation:** Younger bikers show higher accident severity, suggesting overconfidence and less risk awareness.")

        plt.figure(figsize=(12, 7))
        sns.boxplot(x='Accident_Severity', y='Bike_Speed', data=filtered_df, palette='viridis')
        show_plot('Distribution of Bike Speed by Accident Severity', 'Accident Severity', 'Bike Speed')
        st.success("**Interpretation:** Younger bikers show higher accident severity, suggesting overconfidence and less risk awareness.")

        plt.figure(figsize=(12, 7))
        sns.boxplot(x='Accident_Severity', y='Speed_Limit', data=filtered_df, palette='viridis')
        show_plot('Distribution of Speed Limit by Accident Severity', 'Accident Severity', 'Speed Limit')
        st.success("**Interpretation:** Younger bikers show higher accident severity, suggesting overconfidence and less risk awareness.")

        plt.figure(figsize=(12, 7))
        sns.boxplot(x='Biker_Occupation', y='Bike_Speed', data=filtered_df, palette='viridis')
        show_plot('Distribution of Bike Speed by Biker Occupation', 'Biker Occupation', 'Bike Speed', rotation=True)
        st.success("**Interpretation:** Younger bikers show higher accident severity, suggesting overconfidence and less risk awareness.")

    # --- VIOLIN PLOTS ---
    with st.expander("🎻 Violin Plots"):
        plt.figure(figsize=(12, 7))
        sns.violinplot(x='Accident_Severity', y='Biker_Age', data=filtered_df, palette='viridis')
        show_plot('Distribution of Biker Age by Accident Severity (Violin Plot)', 'Accident Severity', 'Biker Age')
        st.success("**Interpretation:** Younger bikers show higher accident severity, suggesting overconfidence and less risk awareness.")

        plt.figure(figsize=(12, 7))
        sns.violinplot(x='Weather', y='Bike_Speed', data=filtered_df, palette='viridis')
        show_plot('Distribution of Bike Speed by Weather (Violin Plot)', 'Weather', 'Bike Speed')
        st.success("**Interpretation:** Younger bikers show higher accident severity, suggesting overconfidence and less risk awareness.")

    # --- SCATTER PLOTS ---
    with st.expander("📈 Scatter Plots"):
        plt.figure(figsize=(14, 10))
        sns.scatterplot(x='Bike_Speed', y='Daily_Travel_Distance', hue='Accident_Severity', data=filtered_df, palette='viridis', alpha=0.6)
        plt.legend(title='Accident Severity')
        show_plot('Daily Travel Distance vs Bike Speed by Accident Severity', 'Bike Speed', 'Daily Travel Distance')
        st.success("**Interpretation:** Younger bikers show higher accident severity, suggesting overconfidence and less risk awareness.")

        plt.figure(figsize=(12, 8))
        sns.scatterplot(x='Bike_Speed', y='Biker_Age', data=filtered_df, alpha=0.6)
        show_plot('Biker Age vs Bike Speed', 'Bike Speed', 'Biker Age')
        st.success("**Interpretation:** Younger bikers show higher accident severity, suggesting overconfidence and less risk awareness.")

        plt.figure(figsize=(12, 8))
        sns.scatterplot(x='Daily_Travel_Distance', y='Biker_Age', data=filtered_df, alpha=0.6)
        show_plot('Biker Age vs Daily Travel Distance', 'Daily Travel Distance', 'Biker Age')
        st.success("**Interpretation:** Younger bikers show higher accident severity, suggesting overconfidence and less risk awareness.")

# --- FOOTER ---
st.markdown("---")
st.caption("© 2025 Motorbike Accident Dashboard | Designed with ❤️ using Streamlit & Plotly")
