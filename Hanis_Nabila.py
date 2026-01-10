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

# =====================================================
# DATASET OVERVIEW
# =====================================================
st.subheader("📌 Key Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Find Info Online",
    f"{(df['Find_Mental_Health_Info_Online']
        .astype(str).isin(['4','5']).mean()*100):.1f}%"
)

col2.metric(
    "Seek Help Online When Stressed",
    f"{(df['Seek_Help_Online_When_Stress']
        .astype(str).isin(['4','5']).mean()*100):.1f}%"
)

col3.metric(
    "Use Online Communities",
    f"{(df['Use_Online_Communities_for_Support']
        .astype(str).isin(['4','5']).mean()*100):.1f}%"
)

col4.metric(
    "Follow Motivational Content",
    f"{(df['Follow_Motivational_Mental_Health_Content']
        .astype(str).isin(['4','5']).mean()*100):.1f}%"
)

st.markdown("---")


# =====================================================
# SUMMARY BOX
# =====================================================
st.subheader("📌 Key Mental Health Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "High Usage (>5 hrs/day)",
    f"{(df['Social_Media_Use_Frequency']
        .isin(['5 to 6 hours per day','More than 6 hours per day'])
        .mean()*100):.1f}%"
)

col2.metric(
    "Often / Always Assignment Stress",
    f"{(df['Assignments_Stress'].astype(str).isin(['4','5']).mean()*100):.1f}%"
)

col3.metric(
    "Sleep Frequently Affected",
    f"{(df['Sleep_Affected_By_Social_Media'].astype(str).isin(['4','5']).mean()*100):.1f}%"
)

col4.metric(
    "Agree Negative Impact",
    f"{(df['Social_Media_Negative_Impact_on_Wellbeing'].astype(str).isin(['4','5']).mean()*100):.1f}%"
)

st.markdown("---")

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
A large proportion of students frequently seek mental health information through online
platforms, highlighting the internet as a primary source of support.
""")

# =====================================================
# ONLINE HELP WHEN STRESSED
# =====================================================
st.subheader("🆘 Preference for Online Help During Stress")

fig = px.histogram(
    df,
    x="Seek_Help_Online_When_Stress",
    title="Preference for Seeking Help Online When Stressed"
)
st.plotly_chart(fig, use_container_width=True)

st.success("""
**Interpretation:**  
Many students show a strong preference for online help during stressful situations,
suggesting digital support is often favoured over face-to-face options.
""")

# =====================================================
# ONLINE COMMUNITIES BY GENDER
# =====================================================
st.subheader("👥 Online Community Support by Gender")

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
Engagement with online support communities varies across genders, indicating
different help-seeking behaviours among students.
""")

# =====================================================
# STRESS vs ONLINE HELP
# =====================================================
st.subheader("Assignment Stress vs Online Help Preference")

stress_map = {'1':'Low','2':'Moderate','3':'Neutral','4':'High','5':'Very High'}

df['Stress_Cat'] = df['Assignments_Stress'].astype(str).map(stress_map)

stress_help_table = pd.crosstab(
    df['Stress_Cat'],
    df['Seek_Help_Online_When_Stress']
)

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(stress_help_table, annot=True, fmt="d", cmap="YlGnBu", ax=ax)
ax.set_title("Assignment Stress vs Online Help Preference")
ax.set_xlabel("Online Help Preference Level")
ax.set_ylabel("Assignment Stress Level")
st.pyplot(fig)

st.success("""
**Interpretation:**  
Students experiencing higher assignment stress are more likely to seek help through
online platforms.
""")

# =====================================================
# STRESS vs ONLINE COMMUNITIES
# =====================================================
st.subheader("🤝 Assignment Stress vs Online Community Usage")

stress_community_table = pd.crosstab(
    df['Stress_Cat'],
    df['Use_Online_Communities_for_Support']
)

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(stress_community_table, annot=True, fmt="d", cmap="YlGnBu", ax=ax)
ax.set_title("Assignment Stress vs Online Community Support")
ax.set_xlabel("Online Community Usage Level")
ax.set_ylabel("Assignment Stress Level")
st.pyplot(fig)

st.success("""
**Interpretation:**  
Higher stress levels correspond with increased reliance on online communities,
emphasising their role as informal mental health support systems.
""")
