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
# DATA TRANSFORMATION (SAFE)
# ==============================

# Short labels
short_label_map = {
    "Less than 1 hour per day": "< 1 hr",
    "1 to 2 hours per day": "1–2 hrs",
    "3 to 4 hours per day": "3–4 hrs",
    "5 to 6 hours per day": "5–6 hrs",
    "More than 6 hours per day": "> 6 hrs"
}

df["Social_Media_Use_Frequency"] = (
    df["Social_Media_Use_Frequency"]
    .map(short_label_map)
)

# Numeric mapping
hours_map = {
    "< 1 hr": 0.5,
    "1–2 hrs": 1.5,
    "3–4 hrs": 3.5,
    "5–6 hrs": 5.5,
    "> 6 hrs": 7
}

df["Daily_Internet_Usage_Hours"] = (
    df["Social_Media_Use_Frequency"]
    .map(hours_map)
)

# ==============================
# CREATE ANALYSIS DATAFRAME
# ==============================
columns_needed = [
    "Social_Media_Use_Frequency",
    "Daily_Internet_Usage_Hours",
    "Assignments_Stress",
    "Academic_Workload_Anxiety",
    "Difficulty_Sleeping_University_Pressure",
    "Social_Media_Negative_Impact_on_Wellbeing",
    "Sleep_Affected_By_Social_Media"
]

df_analysis = df[columns_needed].copy()

# Convert Likert to numeric
likert_cols = [
    "Assignments_Stress",
    "Academic_Workload_Anxiety",
    "Difficulty_Sleeping_University_Pressure",
    "Social_Media_Negative_Impact_on_Wellbeing"
]

for col in likert_cols:
    df_analysis[col] = pd.to_numeric(df_analysis[col], errors="coerce")

# ==============================
# MELT FOR MULTI-FACTOR ANALYSIS
# ==============================
mental_health_map = {
    "Assignments_Stress": "Stress from Assignments",
    "Academic_Workload_Anxiety": "Academic Anxiety",
    "Difficulty_Sleeping_University_Pressure": "Sleep Difficulty",
    "Social_Media_Negative_Impact_on_Wellbeing": "Negative Wellbeing Impact"
}

df_melted = df_analysis.melt(
    id_vars="Daily_Internet_Usage_Hours",
    value_vars=likert_cols,
    var_name="Mental_Health_Factor",
    value_name="Score"
)

df_melted["Mental_Health_Factor"] = (
    df_melted["Mental_Health_Factor"]
    .map(mental_health_map)
)

df_grouped = (
    df_melted
    .dropna()
    .groupby(["Daily_Internet_Usage_Hours", "Mental_Health_Factor"])
    ["Score"]
    .mean()
    .reset_index()
)

# ==============================
# STREAMLIT UI
# ==============================
st.title("Internet Usage & Mental Health Among UMK Students")

# ==============================
# BAR CHART
# ==============================
st.subheader("Mental Health Scores by Internet Usage")

fig_bar = px.bar(
    df_grouped,
    x="Daily_Internet_Usage_Hours",
    y="Score",
    color="Mental_Health_Factor",
    barmode="group",
    labels={
        "Daily_Internet_Usage_Hours": "Daily Internet Usage (Hours)",
        "Score": "Mean Mental Health Score"
    }
)

st.plotly_chart(fig_bar, use_container_width=True)

# ==============================
# BOX PLOT
# ==============================
df_box = df_analysis.copy()

df_box["Sleep_Affected"] = pd.to_numeric(
    df_box["Sleep_Affected_By_Social_Media"],
    errors="coerce"
)

df_box["Sleep_Affected_Label"] = df_box["Sleep_Affected"].apply(
    lambda x: "Yes" if x >= 4 else "No" if x <= 3 else None
)

df_box = df_box.dropna(
    subset=["Sleep_Affected_Label", "Difficulty_Sleeping_University_Pressure"]
)

fig_box = px.box(
    df_box,
    x="Sleep_Affected_Label",
    y="Difficulty_Sleeping_University_Pressure",
    points="all",
    title="Sleep Difficulty vs Social Media Affecting Sleep",
    labels={
        "Sleep_Affected_Label": "Social Media Affects Sleep",
        "Difficulty_Sleeping_University_Pressure": "Sleep Difficulty Score"
    }
)

st.plotly_chart(fig_box, use_container_width=True)

# ==============================
# CORRELATION HEATMAP
# ==============================
st.subheader("Correlation Heatmap")

corr_df = df_analysis[
    ["Daily_Internet_Usage_Hours"] + likert_cols
].dropna()

corr = corr_df.corr()

fig_heatmap = px.imshow(
    corr,
    text_auto=True,
    title="Correlation Between Internet Usage & Mental Health"
)

st.plotly_chart(fig_heatmap, use_container_width=True)

# ==============================
# LINE PLOT
# ==============================
st.subheader("Trend of Mental Health Scores by Internet Usage")

fig_line = px.line(
    df_grouped.sort_values("Daily_Internet_Usage_Hours"),
    x="Daily_Internet_Usage_Hours",
    y="Score",
    color="Mental_Health_Factor",
    markers=True
)

st.plotly_chart(fig_line, use_container_width=True)

# ==============================
# SCATTER PLOTS (SEABORN)
# ==============================
st.subheader("Scatter Plots")

g = sns.relplot(
    data=df_melted.dropna(),
    x="Daily_Internet_Usage_Hours",
    y="Score",
    col="Mental_Health_Factor",
    col_wrap=2,
    kind="scatter",
    height=4
)

st.pyplot(g.fig)

