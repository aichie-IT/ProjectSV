import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

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

# ==============================
# DATA CLEANING
# ==============================

# Standardise column names
df.columns = df.columns.str.strip()

# Fix encoding issues
df = df.replace(
    {"â\x80\x93": "-", "–": "-", "—": "-"},
    regex=True
)

# ==============================
# DATA FILTERING
# ==============================

# Remove irrelevant columns
columns_to_remove = [
    "Timestamp",
    "Type_of_Online_Content_Affects",
    "Universities_Support_Actions"
]

df = df.drop(columns=columns_to_remove, errors="ignore")

# Keep only variables needed for mental health analysis
columns_to_keep = [
    "Gender",
    "Find_Mental_Health_Info_Online",
    "Seek_Help_Online_When_Stress",
    "Use_Online_Communities_for_Support",
    "Assignments_Stress",
    "Follow_Motivational_Mental_Health_Content",
    "Mental_Health_Info_Through_Internet"
]

df = df[columns_to_keep]

# ==============================
# DATA TRANSFORMATION
# ==============================

# Likert scale mapping
likert_map = {
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5
}

# Convert Likert responses to numeric
likert_columns = [
    "Find_Mental_Health_Info_Online",
    "Seek_Help_Online_When_Stress",
    "Use_Online_Communities_for_Support",
    "Assignments_Stress",
    "Follow_Motivational_Mental_Health_Content",
    "Mental_Health_Info_Through_Internet"
]

for col in likert_columns:
    df[col + "_Numeric"] = (
        df[col]
        .astype(str)
        .map(likert_map)
    )

# ==============================
# OUTPUT DATASET
# ==============================

processed_df = df.copy()

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
   
