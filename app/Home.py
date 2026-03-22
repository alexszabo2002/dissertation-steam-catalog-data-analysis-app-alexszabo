import streamlit as st

st.set_page_config(page_title="Home Page", layout="wide")

st.title("Welcome to the Steam Catalog Exploration App!")
st.write("""
This application is designed to analyze the current Steam Catalog. 
You can explore specific games, analyze market trends, and visualize interesting data.
""")

if st.button("🚀 Jump into the Steam Catalog"):
    st.switch_page("pages/01_Catalog.py")
