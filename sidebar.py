import streamlit as st

st.set_page_config(page_title="Students Mental Health Analysis", layout="wide")

# Define Pages
home = st.Page("home.py", title="Home", icon=":material/home:")

internetUsage = st.Page("Nur_Aishah_Sakinah.py", title="Internet Use vs. Mental Health", icon=":material/insights:")
ilya = st.Page("ilya.py", title="Advanced Visualizations", icon=":material/show_chart:")
hanis = st.Page("hanis.py", title="Correlation Insights", icon=":material/share:")
ainun = st.Page("ainun.py", title="Riding Behavior Insights", icon=":material/pedal_bike:")

# Sidebar Navigation
pg = st.navigation({
    "Menu": [home],
    "Motor Accident Severity Analysis": [
        internetUsage,
        ilya,
        hanis,
        ainun
    ]
})

# Run navigation
pg.run()
