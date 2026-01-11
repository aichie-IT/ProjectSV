import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.subheader("Analyze Mental Health Information-Seeking Behavior")

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

likert_numeric_map = {
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5
}

yes_no_map = {
    'Yes': 1,
    'No': 0
}

freq_map = {
    'Never': 1,
    'Rarely': 2,
    'Sometimes': 3,
    'Often': 4
}

    df['Find_Mental_Health_Info_Online_Numeric'] = (
    df['Find_Mental_Health_Info_Online'].astype(str).map(yes_no_map)
    )

    df['Use_Online_Communities_for_Support_Numeric'] = (
    df['Use_Online_Communities_for_Support'].astype(str).map(freq_map)
    )

columns_to_keep = [
    'Gender',
    'Find_Mental_Health_Info_Online',
    'Seek_Help_Online_When_Stress',
    'Use_Online_Communities_for_Support',
    'Assignments_Stress',
    'Follow_Motivational_Mental_Health_Content',
    'Mental_Health_Info_Through_Internet'
]

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

# =====================================================
# SUMMARY BOX
# =====================================================
st.subheader("📌 Key Mental Health Information-Seeking Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Often / Always Assignment Stress",
    f"{(df['Assignments_Stress_Numeric'] >= 4).mean()*100:.1f}%"
)

col2.metric(
    "Actively Search Mental Health Info",
    f"{(df['Find_Mental_Health_Info_Online_Numeric'] >= 4).mean()*100:.1f}%"
)

col3.metric(
    "Prefer Online Help When Stressed",
    f"{(df['Seek_Help_Online_When_Stress_Numeric'] >= 4).mean()*100:.1f}%"
)

col4.metric(
    "Use Online Communities for Support",
    f"{(df['Use_Online_Communities_for_Support_Numeric'] >= 4).mean()*100:.1f}%"
)

st.markdown("---")


# =====================================================
#   Online Help Preference (High vs Low)
# =====================================================
st.subheader("Preference for Online Help (High vs Low)")

df['Online_Help_Level'] = df['Seek_Help_Online_When_Stress'].astype(str).apply(
    lambda x: 'High (Agree)' if x in ['4','5'] else 'Low (Neutral)'
)

pie_data = df['Online_Help_Level'].value_counts().reset_index()
pie_data.columns = ['Preference', 'Count']

fig = px.pie(
    pie_data,
    names='Preference',
    values='Count',
    hole=0.45,
    title="Overall Preference for Seeking Help Online"
)

st.plotly_chart(fig, use_container_width=True)

st.success("""
**Interpretation:**  
The donut chart shows that a huge majority of students, 72.3%, stay in the low or neutral zone. 
Only 27.7% really prefer getting help online regarding this preference. It seems like some 
people really find digital platforms to be their go-to for support.

""")

# =====================================================
# ONLINE COMMUNITIES BY GENDER
# =====================================================
st.subheader("Online Community Support by Gender")

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
Female students consistently outnumber male students across almost all frequency categories, 
most notably in the "Sometimes" category. "Often" category shows 15 female participants but 0 male participants.
This shows that frequent engagement with online support communities is almost exclusively a female behavior in this dataset.
""")

# =====================================================
#   Assignment Stress vs Online Help
# =====================================================
st.subheader("Assignment Stress vs Online Help Preference")

fig = px.box(
    df,
    x="Seek_Help_Online_When_Stress",
    y="Assignments_Stress",
    title="Assignment Stress Levels Across Online Help Preference",
    labels={
        "Seek_Help_Online_When_Stress": "Online Help Preference Level",
        "Assignments_Stress": "Assignment Stress Level"
    }
)

st.plotly_chart(fig, use_container_width=True)

st.success("""
**Interpretation:**  
The box plot shows that students who really want online help (Level 5) also have some of 
the highest stress levels, reaching up to level 5 on the stress scale. Meanwhile, those who 
do not need care for online help (Level 1) usually have lower stress. 
""")

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
This chart shows that shows that "Sometimes" is the most common frequency, with a count of 50. 
This is followed by "Rarely" (20) and "Often" (17). Notably, only a small fraction of the 
group "Always" (8) or "Never" (6) seeks out this information.
This indicates that while most students use the internet for mental health information, 
they do so sporadically rather than as a constant habit.
""")

# =====================================================
# ONLINE HELP WHEN STRESSED
# =====================================================
st.subheader("Preference for Online Help During Stress")

fig = px.histogram(
    df,
    x="Seek_Help_Online_When_Stress",
    title="Preference for Seeking Help Online When Stressed"
)
st.plotly_chart(fig, use_container_width=True)

st.success("""
**Interpretation:**  
The distribution is somewhat bell-shaped but leans toward the middle. The highest 
count is at Level 3 (35 students), indicating a moderate preference. This suggests 
that while students are open to online help when stressed, many maintain a neutral 
or cautious.
""")

# =====================================================
# STRESS vs ONLINE COMMUNITIES
# =====================================================

# Crosstab
heatmap_data = pd.crosstab(
    df['Assignments_Stress'],
    df['Use_Online_Communities_for_Support']
)

# Create figure
fig, ax = plt.subplots()

# Plot heatmap
im = ax.imshow(heatmap_data.values)

# Colorbar
plt.colorbar(im, ax=ax)

# Axis ticks and labels
ax.set_xticks(range(len(heatmap_data.columns)))
ax.set_xticklabels(heatmap_data.columns, rotation=45)

ax.set_yticks(range(len(heatmap_data.index)))
ax.set_yticklabels(heatmap_data.index)

# Add cell values
for i in range(len(heatmap_data.index)):
    for j in range(len(heatmap_data.columns)):
        ax.text(
            j, i,
            heatmap_data.iloc[i, j],
            ha="center",
            va="center"
        )

# Labels and title
ax.set_xlabel("Use Online Communities for Support")
ax.set_ylabel("Stress Level")
ax.set_title("Stress Level vs Use of Online Communities for Support")

# Show in Streamlit
st.pyplot(fig)

st.success("""
**Interpretation:**  
The biggest group is 18 students who have a stress level of 3 and only "Sometimes" 
use online communities for support. Another 16 students have a high stress level of 4 
and also use communities "Sometimes." It’s clear that "Sometimes" is the most popular 
choice for students feeling stress.
""")
