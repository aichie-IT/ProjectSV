import streamlit as st
import pandas as pd
import plotly.express as px

st.subheader("🔥 Social Media Usage vs Assignment Stress")

# Show unique values properly in Streamlit
st.write("Unique values in Assignments Stress:")
st.write(hanis_df['Assignments_Stress'].unique())

# Mapping numerical strings to categorical labels
assignments_stress_mapping = {
    '1': 'Never',
    '2': 'Rarely',
    '3': 'Sometimes',
    '4': 'Often',
    '5': 'Always'
}

# Create a categorical column WITHOUT modifying shared data
hanis_df['Assignments_Stress_Categorical'] = (
    hanis_df['Assignments_Stress']
    .astype(str)
    .map(assignments_stress_mapping)
)

# Create contingency table
contingency_table = pd.crosstab(
    hanis_df['Social_Media_Use_Frequency'],
    hanis_df['Assignments_Stress_Categorical']
)

# Reorder rows
social_media_order = [
    'Less than 1 hour per day',
    '1 to 2 hours per day',
    '3 to 4 hours per day',
    '5 to 6 hours per day',
    'More than 6 hours per day'
]
contingency_table = contingency_table.reindex(social_media_order, fill_value=0)

# Reorder columns
assignments_stress_order = [
    'Never',
    'Rarely',
    'Sometimes',
    'Often',
    'Always'
]
present_cols = [col for col in assignments_stress_order if col in contingency_table.columns]
contingency_table = contingency_table[present_cols]

# Plot heatmap
import matplotlib.pyplot as plt
import seaborn as sns

fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(
    contingency_table,
    annot=True,
    fmt="d",
    cmap="YlGnBu",
    linewidths=0.5,
    ax=ax
)

ax.set_title("Heatmap of Social Media Use Frequency vs Assignment Stress")
ax.set_xlabel("Assignment Stress Level")
ax.set_ylabel("Social Media Use Frequency")

st.pyplot(fig)


st.subheader("😴 Social Media Usage vs Sleep Disruption")

# Show unique values properly
st.write("Unique values in Sleep Affected By Social Media:")
st.write(hanis_df['Sleep_Affected_By_Social_Media'].unique())

# Mapping numerical strings to categorical labels
sleep_affected_mapping = {
    '1': 'Never',
    '2': 'Rarely',
    '3': 'Sometimes',
    '4': 'Often',
    '5': 'Always'
}

# Create categorical column (safe copy)
hanis_df['Sleep_Affected_By_Social_Media_Categorical'] = (
    hanis_df['Sleep_Affected_By_Social_Media']
    .astype(str)
    .map(sleep_affected_mapping)
)

# Create contingency table
contingency_table_sleep = pd.crosstab(
    hanis_df['Social_Media_Use_Frequency'],
    hanis_df['Sleep_Affected_By_Social_Media_Categorical']
)

# Reorder rows
social_media_order = [
    'Less than 1 hour per day',
    '1 to 2 hours per day',
    '3 to 4 hours per day',
    '5 to 6 hours per day',
    'More than 6 hours per day'
]
contingency_table_sleep = contingency_table_sleep.reindex(social_media_order, fill_value=0)

# Reorder columns
sleep_affected_order = [
    'Never',
    'Rarely',
    'Sometimes',
    'Often',
    'Always'
]
present_cols = [col for col in sleep_affected_order if col in contingency_table_sleep.columns]
contingency_table_sleep = contingency_table_sleep[present_cols]

# Plot heatmap
import matplotlib.pyplot as plt
import seaborn as sns

fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(
    contingency_table_sleep,
    annot=True,
    fmt="d",
    cmap="YlGnBu",
    linewidths=0.5,
    ax=ax
)

ax.set_title("Heatmap of Social Media Use Frequency vs Sleep Disruption")
ax.set_xlabel("Sleep Affected by Social Media")
ax.set_ylabel("Social Media Use Frequency")

st.pyplot(fig)


st.subheader("⚖️ Perceived Positive vs Negative Impact of Social Media on Wellbeing")

# Mapping for agreement levels
impact_mapping = {
    '1': 'Strongly Disagree',
    '2': 'Disagree',
    '3': 'Neutral',
    '4': 'Agree',
    '5': 'Strongly Agree'
}

# Create categorical columns (safe copy)
hanis_df['Positive_Impact_Categorical'] = (
    hanis_df['Social_Media_Positive_Impact_on_Wellbeing']
    .astype(str)
    .map(impact_mapping)
)

hanis_df['Negative_Impact_Categorical'] = (
    hanis_df['Social_Media_Negative_Impact_on_Wellbeing']
    .astype(str)
    .map(impact_mapping)
)

# Ensure consistent order of responses
response_order = list(impact_mapping.values())

positive_counts = (
    hanis_df['Positive_Impact_Categorical']
    .value_counts()
    .reindex(response_order, fill_value=0)
)

negative_counts = (
    hanis_df['Negative_Impact_Categorical']
    .value_counts()
    .reindex(response_order, fill_value=0)
)

# Prepare DataFrame for plotting
plot_df = pd.DataFrame({
    'Positive Impact': positive_counts,
    'Negative Impact': negative_counts
}).T

# Plot stacked bar chart
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 7))
plot_df.plot(
    kind='bar',
    stacked=True,
    ax=ax,
    colormap='viridis'
)

ax.set_title("Distribution of Agreement Levels for Social Media Impact on Wellbeing")
ax.set_xlabel("Type of Impact")
ax.set_ylabel("Number of Respondents")
ax.set_xticklabels(plot_df.index, rotation=0)
ax.legend(title="Agreement Level", bbox_to_anchor=(1.05, 1), loc='upper left')

st.pyplot(fig)


st.subheader("📦 Wellbeing Impact Score by Social Media Usage")

# Map numerical strings to numerical values
impact_mapping_numerical = {
    '1': 1,  # Strongly Disagree
    '2': 2,  # Disagree
    '3': 3,  # Neutral
    '4': 4,  # Agree
    '5': 5   # Strongly Agree
}

# Create numerical columns safely
hanis_df['Positive_Impact_Numerical'] = (
    hanis_df['Social_Media_Positive_Impact_on_Wellbeing']
    .astype(str)
    .map(impact_mapping_numerical)
)

hanis_df['Negative_Impact_Numerical'] = (
    hanis_df['Social_Media_Negative_Impact_on_Wellbeing']
    .astype(str)
    .map(impact_mapping_numerical)
)

# Melt DataFrame for plotting
df_melted = hanis_df.melt(
    id_vars=['Social_Media_Use_Frequency'],
    value_vars=['Positive_Impact_Numerical', 'Negative_Impact_Numerical'],
    var_name='Impact_Type',
    value_name='Wellbeing_Impact_Score'
)

# Order Social Media Use Frequency
social_media_order = [
    'Less than 1 hour per day',
    '1 to 2 hours per day',
    '3 to 4 hours per day',
    '5 to 6 hours per day',
    'More than 6 hours per day'
]

df_melted['Social_Media_Use_Frequency'] = pd.Categorical(
    df_melted['Social_Media_Use_Frequency'],
    categories=social_media_order,
    ordered=True
)

# Plot box plot
import matplotlib.pyplot as plt
import seaborn as sns

fig, ax = plt.subplots(figsize=(14, 8))
sns.boxplot(
    x='Social_Media_Use_Frequency',
    y='Wellbeing_Impact_Score',
    hue='Impact_Type',
    data=df_melted,
    ax=ax
)

ax.set_title("Wellbeing Impact Score by Social Media Use Frequency and Impact Type")
ax.set_xlabel("Social Media Use Frequency")
ax.set_ylabel("Wellbeing Impact Score")

ax.set_yticks([1, 2, 3, 4, 5])
ax.set_yticklabels([
    'Strongly Disagree',
    'Disagree',
    'Neutral',
    'Agree',
    'Strongly Agree'
])

ax.tick_params(axis='x', rotation=30)
ax.legend(
    title="Impact Type",
    labels=["Positive Impact", "Negative Impact"],
    loc="upper left"
)

st.pyplot(fig)

