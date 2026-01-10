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

# Continue dropping irrelevant columns
df = df.drop(columns=cols_to_drop, errors="ignore")

# -----------------------------
# Likert mapping (KEEP VARIABLES)
# -----------------------------
likert_numeric_map = {
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5
}

# --- Process X-axis: Internet use before sleep (Yes / No) ---
df['Sleep_Affected_By_Social_Media_Numeric_Str'] = df['Sleep_Affected_By_Social_Media'].astype(str)

def map_sleep_impact_to_binary(response_str):
    try:
        response_int = int(response_str)
        if response_int >= 4:
            return 'Yes'
        elif response_int <= 3:
            return 'No'
    except ValueError:
        return None

df['Internet_Use_Affects_Sleep'] = df['Sleep_Affected_By_Social_Media_Numeric_Str'].apply(
    map_sleep_impact_to_binary
)

# --- Process Y-axis: Mental health score ---
df['Difficulty_Sleeping_University_Pressure_Numeric_Str'] = (
    df['Difficulty_Sleeping_University_Pressure'].astype(str)
)
df['Difficulty_Sleeping_University_Pressure_Score'] = (
    df['Difficulty_Sleeping_University_Pressure_Numeric_Str']
    .map(likert_numeric_map)
)

# Drop invalid rows
df_plot = df.dropna(
    subset=[
        'Internet_Use_Affects_Sleep',
        'Difficulty_Sleeping_University_Pressure_Score'
    ]
).copy()

# -----------------------------
# STREAMLIT + PLOTLY BOXPLOT
# -----------------------------
st.subheader("Difficulty Sleeping vs Social Media Affecting Sleep")

fig = px.box(
    df_plot,
    x='Internet_Use_Affects_Sleep',
    y='Difficulty_Sleeping_University_Pressure_Score',
    category_orders={'Internet_Use_Affects_Sleep': ['No', 'Yes']},
    labels={
        'Internet_Use_Affects_Sleep': 'Social Media Affects Sleep',
        'Difficulty_Sleeping_University_Pressure_Score':
        'Difficulty Sleeping Score (1–5)'
    }
)

fig.update_layout(
    yaxis=dict(dtick=1),
    template='plotly_white'
)

st.plotly_chart(fig, use_container_width=True)


# --- PLOT ---
fig = px.bar(
    df_melted,
    x="Internet_Usage_Category",
    y="Score",
    color="Mental_Health_Factor",
    barmode="group",
    category_orders={"Internet_Usage_Category": order},
    labels={
        "Score": "Mean Score (Likert Scale: 1–5)",
        "Internet_Usage_Category": "Internet Usage Category",
        "Mental_Health_Factor": "Mental Health Factor"
    }
)

fig.update_layout(
    legend_title_text="Mental Health Factor",
    height=600
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Difficulty Sleeping by Social Media Affecting Sleep")

# --- Likert numeric mapping ---
likert_numeric_map = {
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5
}

# --- PROCESS X-AXIS: Internet use affects sleep (Yes / No) ---
df_new["Sleep_Affected_By_Social_Media_Numeric_Str"] = (
    df_new["Sleep_Affected_By_Social_Media"].astype(str)
)

def map_sleep_impact_to_binary(response_str):
    try:
        response_int = int(response_str)
        if response_int >= 4:
            return "Yes"
        elif response_int <= 3:
            return "No"
    except ValueError:
        return None

df_new["Internet_Use_Affects_Sleep"] = (
    df_new["Sleep_Affected_By_Social_Media_Numeric_Str"]
    .apply(map_sleep_impact_to_binary)
)

# --- PROCESS Y-AXIS: Difficulty sleeping score ---
df_new["Difficulty_Sleeping_University_Pressure_Score"] = (
    df_new["Difficulty_Sleeping_University_Pressure"]
    .astype(str)
    .map(likert_numeric_map)
)

# --- CLEAN DATA FOR PLOTTING ---
df_plot = df_new.dropna(
    subset=[
        "Internet_Use_Affects_Sleep",
        "Difficulty_Sleeping_University_Pressure_Score"
    ]
).copy()

# Ensure correct order
df_plot["Internet_Use_Affects_Sleep"] = pd.Categorical(
    df_plot["Internet_Use_Affects_Sleep"],
    categories=["No", "Yes"],
    ordered=True
)

# --- PLOTLY BOX PLOT ---
fig = px.box(
    df_plot,
    x="Internet_Use_Affects_Sleep",
    y="Difficulty_Sleeping_University_Pressure_Score",
    category_orders={"Internet_Use_Affects_Sleep": ["No", "Yes"]},
    labels={
        "Internet_Use_Affects_Sleep": "Social Media Affects Sleep",
        "Difficulty_Sleeping_University_Pressure_Score":
            "Difficulty Sleeping Score (1–5)"
    }
)

fig.update_layout(
    height=500,
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)
