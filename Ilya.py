import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st

# --- LOAD DATA ---
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQnrGG72xRS-qLoiM2zon4eP8t5XMiO5MhoLUEe2jJer0G5EzodiU4e0NOmx_ssmCwZf-AnbQXhBbTM/pub?gid=1791189796&single=true&output=csv"
    return pd.read_csv(url)

df = load_data()

## Clean Column Names
df.columns = df.columns.str.strip()

# Rename Columns (your renaming logic stays the same)
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

# Transforming the Likert scale responses
likert_numeric_map = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5}
likert_cols = [
    'Find_Mental_Health_Info_Online',
    'Seek_Help_Online_When_Stress',
    'Use_Online_Communities_for_Support',
    'Assignments_Stress',
    'Follow_Motivational_Mental_Health_Content',
    'Mental_Health_Info_Through_Internet'
]

for col in likert_cols:
    df[col + "_Numeric"] = df[col].astype(str).map(likert_numeric_map)

# --- Streamlit Tabs ---
tab = st.selectbox("Choose Tab", ["General Visualizations", "Detailed Analysis"])

# General Visualizations Tab
if tab == "General Visualizations":
    st.title("General Visualizations")

    st.subheader("📌 Key Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Find Info Online", f"{(df['Find_Mental_Health_Info_Online'].astype(str).isin(['4','5']).mean()*100):.1f}%")
    col2.metric("Seek Help Online When Stressed", f"{(df['Seek_Help_Online_When_Stress'].astype(str).isin(['4','5']).mean()*100):.1f}%")
    col3.metric("Use Online Communities", f"{(df['Use_Online_Communities_for_Support'].astype(str).isin(['4','5']).mean()*100):.1f}%")
    col4.metric("Follow Motivational Content", f"{(df['Follow_Motivational_Mental_Health_Content'].astype(str).isin(['4','5']).mean()*100):.1f}%")
    
    st.markdown("---")

    # Online Mental Health Information
    st.subheader("Seeking Mental Health Information Online")
    fig = px.histogram(df, x="Mental_Health_Info_Through_Internet", title="Frequency of Seeking Mental Health Information Online")
    st.plotly_chart(fig)

    st.success("**Interpretation:** A large proportion of students frequently seek mental health information through online platforms.")

    # Online Help When Stressed
    st.subheader("🆘 Preference for Online Help During Stress")
    fig = px.histogram(df, x="Seek_Help_Online_When_Stress", title="Preference for Seeking Help Online When Stressed")
    st.plotly_chart(fig)

    st.success("**Interpretation:** Many students show a strong preference for online help during stressful situations.")

# Detailed Analysis Tab
if tab == "Detailed Analysis":
    st.title("Detailed Analysis")
    st.write("""Analyzing how different patterns of internet use, such as daily usage duration, frequency, and usage before sleep, are associated with indicators of mental health, including stress, anxiety, and depression, among UMK students.""")

    # --- Grouped Bar Chart ---
    st.subheader("Average Mental Health Scores by Internet Usage Level")
    fig, ax = plt.subplots(figsize=(12, 7))
    sns.barplot(x='Internet_Usage_Category', y='Score', hue='Mental_Health_Factor', data=df, errorbar=None, order=['Low', 'Moderate', 'High'], ax=ax)
    ax.set_title('Average Mental Health Scores by Internet Usage Level')
    ax.set_xlabel('Internet Usage Category')
    ax.set_ylabel('Mean Score (Likert Scale: 1=Strongly Disagree, 5=Strongly Agree)')
    ax.legend(title='Mental Health Factor', bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig)

    # --- Box Plot ---
    st.subheader("Difficulty Sleeping Due to University Pressure by Social Media Affecting Sleep")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.boxplot(x='Internet_Use_Affects_Sleep', y='Difficulty_Sleeping_University_Pressure_Score', data=df, palette='magma', order=['No', 'Yes'], ax=ax)
    ax.set_title('Difficulty Sleeping Due to University Pressure by Social Media Affecting Sleep')
    ax.set_xlabel('Social Media Affects Sleep (Yes/No)')
    ax.set_ylabel('Difficulty Sleeping Score (1=Strongly Disagree, 5=Strongly Agree)')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)


