import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# =====================================================
# PAGE TITLE
# =====================================================
st.title("📊 Social Media Impact on Mental Health")
st.markdown("Exploring the relationship between internet use and student wellbeing.")

# =====================================================
# GET DATA FROM SESSION STATE
# =====================================================
if "df" not in st.session_state:
    st.error("Dataset not found. Please load data from the main page first.")
    st.stop()

df = st.session_state["df"].copy()

# =====================================================
# DATASET OVERVIEW
# =====================================================
st.header("📋 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Records", len(df))
col2.metric("Average Age", f"{df['Age'].mean():.1f}")
col3.metric("Top Academic Performance", df['General_Academic_Performance'].mode()[0])
col4.metric("Top Social Media Usage", df['Social_Media_Use_Frequency'].mode()[0])

with st.expander("View Dataset Preview"):
    st.dataframe(df.head(20), use_container_width=True)

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
