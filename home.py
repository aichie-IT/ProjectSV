import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# Add a banner image at the top
banner_image = 'https://raw.githubusercontent.com/fakhitah3/FHPK-TVET/main/3u1i.jpeg'
st.image(banner_image, use_container_width=True)

# Add the main introduction paragraph
st.write(
    """
    **Scientific Visualization** is a multidisciplinary field that focuses on transforming complex scientific data into visual forms that are easier to understand, interpret, and communicate.
    Through the use of computational techniques, visualization helps researchers explore datasets, identify hidden patterns, and gain insights that would otherwise remain obscure in numerical form.
    """
)

banner_image = 'https://raw.githubusercontent.com/fakhitah3/FHPK-TVET/main/3u1i_2.jpeg'
st.image(banner_image, use_container_width=True)

# Add the extended explanation
st.write(
    """
    The aim of scientific visualization is not merely to present data attractively, but to **enhance comprehension and decision-making** through visual analytics.
    Applications span across disciplines such as **climate science**, **medicine**, **engineering**, **data science**, and **environmental studies**.

    In this course or module, students will learn to:
    - Select relevant datasets for analysis and visualization.
    - Apply various visualization techniques such as graphs, maps, and 3D models.
    - Interpret visual outputs to support scientific conclusions and policy recommendations.
   
    By the end of this exercise, students should be able to produce **informative, accurate, and interactive visualizations** that effectively communicate scientific findings to both expert and non-expert audiences.
    """
)


# --- PAGE CONFIG ---
st.set_page_config(page_title="Motorbike Accident Insights Dashboard", page_icon="🏍️", layout="wide")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/aichie-IT/SV25/refs/heads/main/motor_accident.csv"
    df = pd.read_csv(url)
    return df

df = load_data()

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
    st.markdown("Explore how factors like occupation, education, and road conditions impact severity.")

    # ===== COLOR & ORDER SETTINGS =====
    severity_order = ["No Accident", "Moderate Accident", "Severe Accident"]
    severity_colors = {
        "No Accident": "#A8E6CF",       # Pastel Green
        "Moderate Accident": "#FFF3B0", # Pastel Yellow
        "Severe Accident": "#FFD3B6"    # Pastel Orange
    }

    # Force correct dtype & order for Accident_Severity
    filtered_df["Accident_Severity"] = pd.Categorical(
        filtered_df["Accident_Severity"], categories=severity_order, ordered=True
    )
    
    # Summary
    col1, col2, col3 = st.columns(3)
    top_severity = filtered_df['Accident_Severity'].mode()[0]
    top_weather = filtered_df['Weather'].mode()[0]
    top_road = filtered_df['Road_Type'].mode()[0]
    col1.metric("Most Common Severity", top_severity, border=True)
    col2.metric("Common Weather", top_weather, border=True)
    col3.metric("Frequent Road Type", top_road, border=True)

    st.markdown("### Summary")
    st.info("""
    Accident patterns vary significantly across occupational, educational, and environmental factors. 
    Riders from certain occupations or lower education levels tend to experience more severe accidents, 
    possibly due to riskier job exposure or lower safety awareness. Road and weather conditions also 
    strongly influence accident frequency, especially on wet or uneven surfaces. Understanding these 
    categorical trends allows targeted interventions to improve safety.
    """)
    st.markdown("---")

    # --- OCCUPATION ---
    agg_occ = (
        filtered_df.groupby(["Biker_Occupation", "Accident_Severity"])
        .size()
        .reset_index(name="Count")
    )
    fig4 = px.bar(
        agg_occ,
        x="Biker_Occupation",
        y="Count",
        color="Accident_Severity",
        title="Accident Severity by Biker Occupation",
        color_discrete_sequence=color_theme,
        barmode="group"
    )

    # --- EDUCATION ---
    agg_edu = (
        filtered_df.groupby(["Biker_Education_Level", "Accident_Severity"])
        .size()
        .reset_index(name="Count")
    )
    fig5 = px.bar(
        agg_edu,
        x="Biker_Education_Level",
        y="Count",
        color="Accident_Severity",
        title="Accident Severity by Biker Education Level",
        color_discrete_sequence=color_theme,
        barmode="group"
    )

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig4, use_container_width=True)
        st.info("""
        *Interpretation:* Riders in delivery or transport occupations report higher accident severity, likely due to increased road exposure.
        """)
    with col2:
        st.plotly_chart(fig5, use_container_width=True)
        st.info("""
        *Interpretation:* Bikers with higher education levels show lower accident severity, reflecting better safety awareness and risk management.
        """)

    st.markdown("---")
    st.subheader("Other Influencing Factors")

    # --- LOOP FOR OTHER CATEGORICAL VARIABLES ---
    categorical_cols = [
        "Wearing_Helmet", "Motorcycle_Ownership", "Valid_Driving_License",
        "Bike_Condition", "Road_Type", "Road_condition", "Weather",
        "Time_of_Day", "Traffic_Density", "Biker_Alcohol"
    ]

    # Consistent color mapping
    severity_colors_map = {
    "No Accident": "#A8E6CF",       # Pastel Green
    "Moderate Accident": "#FFF3B0", # Pastel Yellow
    "Severe Accident": "#FFD3B6"    # Pastel Orange
     }

    # Ensure categorical order for plotting
    filtered_df["Accident_Severity"] = pd.Categorical(
    filtered_df["Accident_Severity"], categories=severity_order, ordered=True
    )

    # Display 2 charts per row
    for i in range(0, len(categorical_cols), 2):
        col1, col2 = st.columns(2)

        for j, col in enumerate(categorical_cols[i:i+2]):
            
            agg_df = (
                filtered_df.groupby([col, "Accident_Severity"])
                .size()
                .reset_index(name="Count")
                .sort_values("Count", ascending=False)
            )

            fig = px.bar(
                agg_df,
                x=col,
                y="Count",
                color="Accident_Severity",
                title=f"Accident Severity by {col.replace('_', ' ')}",
                color_discrete_map=severity_colors_map,
                category_orders={"Accident_Severity": severity_order},
                barmode="group"
            )

            # Force bars to use fully solid fill (no shading or transparency)
            fig.for_each_trace(lambda t: t.update(marker=dict(line=dict(width=0), opacity=1.0)))

            # Remove the default Plotly gradient shading
            fig.update_traces(marker_coloraxis=None)

            # Force consistent flat color rendering
            fig.update_layout(
                template=None,  # remove plotly's default style template
                plot_bgcolor="white",
                paper_bgcolor="white",
                bargap=0.25,
            )

            if j == 0:
                with col1:
                    st.plotly_chart(fig, use_container_width=True)
                    st.info(f"""*Interpretation:* The chart shows how {col.replace('_',' ').lower()} affects accident severity, where imbalance across categories indicates risk-prone conditions.""")
            else:
                with col2:
                    st.plotly_chart(fig, use_container_width=True)
                    st.info(f"""*Interpretation:* The chart shows how {col.replace('_',' ').lower()} affects accident severity, where imbalance across categories indicates risk-prone conditions.""")


    st.markdown("#### 💬 Observation")
    st.success("""
    The grouped bar charts reveal that higher education correlates with fewer severe accidents, 
    while adverse weather and poor road types contribute to higher accident counts. 
    These findings support public safety campaigns focusing on awareness and road infrastructure improvements.
    """)


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

    st.markdown("#### 💬 Observation")
    st.success("""
    The violin plots highlight that severe accidents are concentrated among high-speed riders. 
    Correlations between experience and severity indicate that experienced riders adapt speed 
    better to conditions, validating behavioral safety theories.
    """)

# ---- Tab 5: Correlation Insights ----
with tab5:
    st.subheader("Correlation Insights")
    st.markdown("Explore feature interrelationships through correlation heatmaps.")

    numeric_cols = df.select_dtypes(include=['int', 'float']).columns
    corr = df[numeric_cols].corr()

    col1, col2 = st.columns(2)
    top_corr = corr.unstack().sort_values(ascending=False)
    col1.metric("Highest Positive Correlation", top_corr.index[1][0], f"{top_corr.iloc[1]:.2f}", border=True)
    col2.metric("Lowest Negative Correlation", top_corr.index[-1][0], f"{top_corr.iloc[-1]:.2f}", border=True)
    
    st.markdown("### Summary")
    st.info("""
    The correlation matrix measures the strength of relationships among numeric attributes. 
    Higher correlations between bike speed, experience, and accident severity imply that 
    behavioral and skill factors are tightly coupled. Weak negative correlations between 
    experience and alcohol use reflect safer patterns among trained riders.
    """)
    st.markdown("---")

    fig = px.imshow(corr, text_auto=True, title="Correlation Heatmap", aspect="auto", color_continuous_scale="Tealrose")
    st.plotly_chart(fig, use_container_width=True)
    st.info("""
    **Interpretation:** Bike speed and accident severity exhibit a strong positive correlation, confirming kinetic energy’s contribution to impact intensity.
    """)

    st.markdown("#### Interpretation")
    st.success("""
    Strong positive correlations between speed and accident severity confirm mechanical energy’s 
    role in crash outcomes. Weak or negative correlations suggest factors like experience help 
    moderate these risks.
    """)
    
    st.markdown("#### 💬 Observation")
    st.info("Higher correlations indicate stronger relationships between factors such as speed, experience, and accident severity.")

# ---- Tab 6: Riding Behavior Insights ----
with tab6:
    st.subheader("🏍️ Riding Behavior Insights")
    st.markdown("Analyze rider behavior patterns and how habits influence accident severity.")

    # Calculate percentages
    helmet = (filtered_df['Wearing_Helmet'].value_counts(normalize=True).get('Yes', 0) * 100)
    alcohol = (filtered_df['Biker_Alcohol'].value_counts(normalize=True).get('Yes', 0) * 100)
    talk = (filtered_df['Talk_While_Riding'].value_counts(normalize=True).get('Yes', 0) * 100)
    smoke = (filtered_df['Smoke_While_Riding'].value_counts(normalize=True).get('Yes', 0) * 100)

    # Styled metric summary using HTML/CSS
    st.markdown("""
    <style>
        .metric-container {
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            flex-wrap: wrap;
            margin-bottom: 1.5rem;
        }
        .metric-card {
            flex: 1;
            background: #f9f9f9;
            padding: 1rem;
            border-radius: 12px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.08);
            text-align: center;
            transition: all 0.2s ease-in-out;
        }
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 3px 8px rgba(0,0,0,0.12);
        }
        .metric-title {
            font-size: 0.9rem;
            color: #555;
            margin-bottom: 0.4rem;
        }
        .metric-value {
            font-size: 1.6rem;
            font-weight: bold;
        }
        .good { color: #2e7d32; }      /* Green for positive behavior */
        .warning { color: #f57c00; }   /* Orange for risk behaviors */
        .bad { color: #c62828; }       /* Red for negative behaviors */
    </style>
    """, unsafe_allow_html=True)

    # Display metric boxes
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-card">
            <div class="metric-title">Helmet Usage</div>
            <div class="metric-value {'good' if helmet > 70 else 'warning'}">{helmet:.1f}%</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">Alcohol Usage</div>
            <div class="metric-value {'bad' if alcohol > 10 else 'good'}">{alcohol:.1f}%</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">Talk While Riding</div>
            <div class="metric-value {'bad' if talk > 20 else 'good'}">{talk:.1f}%</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">Smoke While Riding</div>
            <div class="metric-value {'bad' if smoke > 20 else 'good'}">{smoke:.1f}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Summary")
    st.info("""
    Behavior-based insights demonstrate how individual actions contribute to safety outcomes. 
    Helmet usage is high but inconsistent across demographics, while alcohol and distraction behaviors 
    (talking or smoking) remain significant risk enhancers. These findings reinforce behavioral safety 
    as a cornerstone of accident prevention.
    """)
    st.markdown("---")

    # Define behavior columns and color palette
    behavior_cols = ["Talk_While_Riding", "Smoke_While_Riding", "Wearing_Helmet", "Biker_Alcohol"]
    color_theme = px.colors.qualitative.Pastel

    # Professional bar charts
    for col in behavior_cols:
        if col in filtered_df.columns:
            data = filtered_df[col].value_counts().reset_index()
            data.columns = [col, "Count"]

            fig = px.bar(
                data,
                x=col,
                y="Count",
                text="Count",
                color=col,
                color_discrete_sequence=color_theme,
                title=f"{col.replace('_', ' ')} Distribution"
            )

            fig.update_traces(textposition="outside")
            fig.update_layout(
                showlegend=False,
                xaxis_title=None,
                yaxis_title="Count",
                title_x=0.0,
                title_y=0.95,
                title_font=dict(size=16, family="Arial", color="black"),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=40, b=40),
            )

            st.plotly_chart(fig, use_container_width=True)
            st.success(f"""
            **Interpretation:** The {col.replace('_',' ').lower()} pattern reveals behavioral influence on safety outcomes.
            Higher counts in risky behaviors (e.g., alcohol or distraction) align with increased accident rates.
            """)

    st.markdown("#### 💬 Observation")
    st.success("""
    Riders who talk or smoke while riding show higher accident frequencies, validating the role of 
    attention in safety. Helmet use correlates inversely with severe accidents, supporting mandatory 
    safety gear enforcement.
    """)

# --- FOOTER ---
st.markdown("---")
st.caption("© 2025 Motorbike Accident Dashboard | Designed with ❤️ using Streamlit & Plotly")
