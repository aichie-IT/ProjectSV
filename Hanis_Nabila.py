import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# ================= HELPER FUNCTION =================
def safe_corr(df, col_x, col_y):
    if col_x not in df.columns or col_y not in df.columns:
        return None
    temp = df[[col_x, col_y]].dropna()
    if len(temp) < 3:
        return None
    return temp.corr().iloc[0, 1]

# ================= TITLE =================
st.title("Exploring the Relationship Between Internet Use and Mental Health.")

# ================= RENAME COLUMNS =================
df = df.rename(columns={
    "Age / Umur:": "Age",
    "Gender / Jantina:": "Gender",
    "How often do you use social media? / Berapa kerap anda menggunakan media sosial?": "Social_Media_Use_Frequency",
    "I have been feeling stressed or overwhelmed with assignments. / Saya telah berasa tertekan atau terbeban dengan tugasan.": "Assignments_Stress",
    "Social media has affected my sleep (sleeping late or difficulty sleeping). / Media sosial telah menjejaskan tidur saya (tidur lewat atau sukar tidur).": "Sleep_Affected_By_Social_Media",
    "Social media has a generally positive impact on my wellbeing. / Media sosial secara amnya mempunyai kesan positif terhadap kesejahteraan saya.": "Social_Media_Positive_Impact_on_Wellbeing",
    "Social media has a generally negative impact on my wellbeing. / Media sosial secara amnya mempunyai kesan negatif terhadap kesejahteraan saya.": "Social_Media_Negative_Impact_on_Wellbeing",
    "How would you describe your general academic performance? / Bagaimanakah anda menerangkan prestasi akademik umum anda?": "General_Academic_Performance"
})

# ================= OVERALL SUMMARY =================
st.header("📋 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Records", len(df))
col2.metric("Average Age", f"{df['Age'].mean():.1f}")
col3.metric("Top Academic Performance", df['General_Academic_Performance'].mode()[0])
col4.metric("Top Social Media Usage", df['Social_Media_Use_Frequency'].mode()[0])

with st.expander("View Dataset Preview"):
    st.dataframe(df.head(20), use_container_width=True)

st.markdown("---")

# ================= HANIS NABILA SECTION =================
st.header("📊 Social Media Impact on Mental Health")

hanis_df = df.copy()

# ================= SUMMARY BOX =================
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "High Usage (>5 hrs/day)",
    f"{(hanis_df['Social_Media_Use_Frequency']
        .isin(['5 to 6 hours per day','More than 6 hours per day'])
        .mean()*100):.1f}%"
)

col2.metric(
    "Often/Always Assignment Stress",
    f"{(hanis_df['Assignments_Stress'].astype(str).isin(['4','5']).mean()*100):.1f}%"
)

col3.metric(
    "Sleep Frequently Affected",
    f"{(hanis_df['Sleep_Affected_By_Social_Media'].astype(str).isin(['4','5']).mean()*100):.1f}%"
)

col4.metric(
    "Agree Negative Impact",
    f"{(hanis_df['Social_Media_Negative_Impact_on_Wellbeing'].astype(str).isin(['4','5']).mean()*100):.1f}%"
)

st.markdown("---")

# ================= ASSIGNMENT STRESS =================
st.subheader("📈 Assignment Stress Distribution")

fig = px.histogram(
    hanis_df,
    x="Assignments_Stress",
    title="Distribution of Assignment Stress Levels"
)
st.plotly_chart(fig, use_container_width=True)

st.success("""
**Interpretation:**  
Most students experience moderate to high assignment stress, indicating that academic
workload is a significant mental health factor.
""")

# ================= HEATMAP: STRESS VS SOCIAL MEDIA =================
stress_map = {'1':'Never','2':'Rarely','3':'Sometimes','4':'Often','5':'Always'}
hanis_df['Assignments_Stress_Cat'] = hanis_df['Assignments_Stress'].astype(str).map(stress_map)

contingency = pd.crosstab(
    hanis_df['Social_Media_Use_Frequency'],
    hanis_df['Assignments_Stress_Cat']
)

fig, ax = plt.subplots(figsize=(12, 7))
sns.heatmap(contingency, annot=True, fmt="d", cmap="YlGnBu", ax=ax)
ax.set_title("Social Media Usage vs Assignment Stress")
st.pyplot(fig)

st.success("""
**Interpretation:**  
Higher social media usage is associated with higher assignment stress levels.
""")

# ================= SLEEP DISRUPTION =================
st.subheader("😴 Social Media Usage vs Sleep Disruption")

hanis_df['Sleep_Cat'] = hanis_df['Sleep_Affected_By_Social_Media'].astype(str).map(stress_map)

sleep_table = pd.crosstab(
    hanis_df['Social_Media_Use_Frequency'],
    hanis_df['Sleep_Cat']
)

fig, ax = plt.subplots(figsize=(12, 7))
sns.heatmap(sleep_table, annot=True, fmt="d", cmap="YlGnBu", ax=ax)
ax.set_title("Social Media Usage vs Sleep Disruption")
st.pyplot(fig)

st.success("""
**Interpretation:**  
Students who use social media longer hours are more likely to experience sleep disruption.
""")

# ================= POSITIVE VS NEGATIVE IMPACT =================
st.subheader("⚖️ Positive vs Negative Impact on Wellbeing")

impact_map = {'1':'Strongly Disagree','2':'Disagree','3':'Neutral','4':'Agree','5':'Strongly Agree'}

pos = hanis_df['Social_Media_Positive_Impact_on_Wellbeing'].astype(str).map(impact_map).value_counts()
neg = hanis_df['Social_Media_Negative_Impact_on_Wellbeing'].astype(str).map(impact_map).value_counts()

impact_df = pd.DataFrame({'Positive Impact': pos, 'Negative Impact': neg}).fillna(0)

fig, ax = plt.subplots(figsize=(10, 6))
impact_df.plot(kind='bar', stacked=True, ax=ax)
ax.set_title("Perceived Impact of Social Media on Wellbeing")
st.pyplot(fig)

st.success("""
**Interpretation:**  
Social media has both positive and negative effects on student wellbeing, showing a dual impact.
""")

# ================= WELLBEING SCORE =================
st.subheader("📦 Wellbeing Score by Social Media Usage")

num_map = {'1':1,'2':2,'3':3,'4':4,'5':5}
hanis_df['Positive_Num'] = hanis_df['Social_Media_Positive_Impact_on_Wellbeing'].astype(str).map(num_map)
hanis_df['Negative_Num'] = hanis_df['Social_Media_Negative_Impact_on_Wellbeing'].astype(str).map(num_map)

melted = hanis_df.melt(
    id_vars='Social_Media_Use_Frequency',
    value_vars=['Positive_Num','Negative_Num'],
    var_name='Impact_Type',
    value_name='Score'
)

fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(data=melted, x='Social_Media_Use_Frequency', y='Score', hue='Impact_Type', ax=ax)
ax.set_title("Wellbeing Score by Social Media Usage")
ax.tick_params(axis='x', rotation=30)
st.pyplot(fig)

st.success("""
**Interpretation:**  
Higher social media usage shows greater variability in negative wellbeing scores,
indicating increased mental health risks.
""")

