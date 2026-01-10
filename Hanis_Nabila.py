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

# ========
st.sidebar.markdown("### 📌 Goal 8 Summary")

high_online_info = (
    df['Mental_Health_Info_Through_Internet']
    .astype(str).isin(['3', '4']).mean() * 100
)

st.sidebar.metric(
    "Frequent Online Info Seeking (%)",
    f"{high_online_info:.1f}%"
)
# =====================================================
# DATASET OVERVIEW
# =====================================================
st.header("🧠 Goal 8: Mental Health Information-Seeking Behaviour")

col1, col2, col3 = st.columns(3)

col1.metric("Total Responses", len(df))
col2.metric(
    "Prefer Online Help (%)",
    f"{(df['Seek_Help_Online_When_Stress'].astype(str).isin(['4','5']).mean()*100):.1f}%"
)
col3.metric(
    "Use Online Communities (%)",
    f"{(df['Use_Online_Communities_for_Support'].astype(str).isin(['4','5']).mean()*100):.1f}%"
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

#==========
st.subheader("📌 Key Information-Seeking Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Seek Info Online",
    f"{(df['Mental_Health_Info_Through_Internet']
        .astype(str).isin(['3','4']).mean()*100):.1f}%"
)

col2.metric(
    "Online Help When Stressed",
    f"{(df['Seek_Help_Online_When_Stress']
        .astype(str).isin(['4','5']).mean()*100):.1f}%"
)

col3.metric(
    "Online Communities",
    f"{(df['Use_Online_Communities_for_Support']
        .astype(str).isin(['4','5']).mean()*100):.1f}%"
)

col4.metric(
    "High Assignment Stress",
    f"{(df['Assignments_Stress']
        .astype(str).isin(['4','5']).mean()*100):.1f}%"
)

st.markdown("---")


# =====================================================
# ASSIGNMENT STRESS DISTRIBUTION
# =====================================================
st.subheader("📈 Assignment Stress Distribution")

fig = px.histogram(
    df,
    x="Assignments_Stress",
    title="Distribution of Assignment Stress Levels"
)
st.plotly_chart(fig, use_container_width=True)

st.success("""
**Interpretation:**  
Most students report moderate to high levels of assignment stress, indicating that academic
pressure is a common mental health concern.
""")

# =====================================================
# HEATMAP: SOCIAL MEDIA VS STRESS
# =====================================================
stress_map = {'1':'Never','2':'Rarely','3':'Sometimes','4':'Often','5':'Always'}
df['Assignments_Stress_Cat'] = df['Assignments_Stress'].astype(str).map(stress_map)

stress_table = pd.crosstab(
    df['Social_Media_Use_Frequency'],
    df['Assignments_Stress_Cat']
)

fig, ax = plt.subplots(figsize=(12, 7))
sns.heatmap(stress_table, annot=True, fmt="d", cmap="YlGnBu", ax=ax)
ax.set_title("Social Media Usage vs Assignment Stress")
ax.set_xlabel("Assignment Stress Level")
ax.set_ylabel("Social Media Usage")
st.pyplot(fig)

st.success("""
**Interpretation:**  
Higher social media usage is associated with higher levels of assignment stress.
""")

# =====================================================
# SLEEP DISRUPTION
# =====================================================
st.subheader("😴 Social Media Usage vs Sleep Disruption")

df['Sleep_Cat'] = df['Sleep_Affected_By_Social_Media'].astype(str).map(stress_map)

sleep_table = pd.crosstab(
    df['Social_Media_Use_Frequency'],
    df['Sleep_Cat']
)

fig, ax = plt.subplots(figsize=(12, 7))
sns.heatmap(sleep_table, annot=True, fmt="d", cmap="YlGnBu", ax=ax)
ax.set_title("Social Media Usage vs Sleep Disruption")
ax.set_xlabel("Sleep Affected Level")
ax.set_ylabel("Social Media Usage")
st.pyplot(fig)

st.success("""
**Interpretation:**  
Students who spend more time on social media are more likely to experience sleep disruption.
""")

# =====================================================
# POSITIVE VS NEGATIVE IMPACT
# =====================================================
st.subheader("⚖️ Positive vs Negative Impact on Wellbeing")

impact_map = {
    '1':'Strongly Disagree',
    '2':'Disagree',
    '3':'Neutral',
    '4':'Agree',
    '5':'Strongly Agree'
}

pos = df['Social_Media_Positive_Impact_on_Wellbeing'].astype(str).map(impact_map).value_counts()
neg = df['Social_Media_Negative_Impact_on_Wellbeing'].astype(str).map(impact_map).value_counts()

impact_df = pd.DataFrame({
    'Positive Impact': pos,
    'Negative Impact': neg
}).fillna(0)

fig, ax = plt.subplots(figsize=(10, 6))
impact_df.plot(kind='bar', stacked=True, ax=ax)
ax.set_title("Perceived Impact of Social Media on Wellbeing")
ax.set_ylabel("Number of Students")
st.pyplot(fig)

st.success("""
**Interpretation:**  
Social media plays a dual role, offering both positive support and negative mental health effects.
""")

# =====================================================
# WELLBEING SCORE
# =====================================================
st.subheader("📦 Wellbeing Score by Social Media Usage")

num_map = {'1':1,'2':2,'3':3,'4':4,'5':5}

df['Positive_Num'] = df['Social_Media_Positive_Impact_on_Wellbeing'].astype(str).map(num_map)
df['Negative_Num'] = df['Social_Media_Negative_Impact_on_Wellbeing'].astype(str).map(num_map)

melted = df.melt(
    id_vars='Social_Media_Use_Frequency',
    value_vars=['Positive_Num','Negative_Num'],
    var_name='Impact_Type',
    value_name='Score'
)

fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(
    data=melted,
    x='Social_Media_Use_Frequency',
    y='Score',
    hue='Impact_Type',
    ax=ax
)
ax.set_title("Wellbeing Impact Score by Social Media Usage")
ax.tick_params(axis='x', rotation=30)
st.pyplot(fig)

st.success("""
**Interpretation:**  
Higher social media usage shows greater variability in negative wellbeing scores,
suggesting increased mental health risks.
""")
