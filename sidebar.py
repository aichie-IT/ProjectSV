import streamlit as st

st.set_page_config(page_title="Students Mental Health Analysis", layout="wide")

# Define Pages
home = st.Page("home.py", title="Home", icon=":material/home:")

internetUsage = st.Page("Nur_Aishah_Sakinah.py", title="Internet Use vs. Mental Health", icon=":material/insights:")
ilya = st.Page("Ilya.py", title="Relationship Between Internet Usage and Mental Health Outcomes", icon=":material/show_chart:")
hanis = st.Page("Hanis_Nabila.py", title="Correlation Insights", icon=":material/share:")
ainun = st.Page("Ainun.py", title="Demographic Differences with Mental Health Experiences", icon=":material/insights:")

# Sidebar Navigation
pg = st.navigation({
    "Menu": [home],
    "Students Wellbeings Analysis": [
        internetUsage,
        ilya,
        hanis,
        ainun
    ]
})

# Run navigation
pg.run()
