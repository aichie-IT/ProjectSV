import streamlit as st
import pandas as pd
import plotly.express as px

# Display unique values (optional, for checking)
st.write("Unique Assignments Stress values:")
st.write(df['Assignments_Stress'].unique())

# Map numerical strings to categorical labels
assignments_stress_mapping = {
    '1': 'Never',
    '2': 'Rarely',
    '3': 'Sometimes',
    '4': 'Often',
    '5': 'Always'
}

df['Assignments_Stress_Categorical'] = df['Assignments_Stress'].map(assignments_stress_mapping)

# Create contingency table
contingency_table = pd.crosstab(
    df['Social_Media_Use_Frequency'],
    df['Assignments_Stress_Categorical']
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
present_cols = [c for c in assignments_stress_order if c in contingency_table.columns]
contingency_table = contingency_table[present_cols]

# Convert to long format for Plotly
heatmap_df = contingency_table.reset_index().melt(
    id_vars='Social_Media_Use_Frequency',
    var_name='Assignments Stress',
    value_name='Count'
)

# Plot heatmap using Plotly Express
fig = px.imshow(
    contingency_table,
    text_auto=True,
    color_continuous_scale='YlGnBu',
    labels=dict(
        x="Assignments Stress",
        y="Social Media Use Frequency",
        color="Count"
    )
)

fig.update_layout(
    title="Heatmap of Social Media Use Frequency vs. Assignments Stress",
    xaxis_title="Assignments Stress",
    yaxis_title="Social Media Use Frequency"
)

# Display in Streamlit
st.plotly_chart(fig, use_container_width=True)

