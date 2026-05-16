import streamlit as st
import plotly.express as px
from utils.opportunity_analysis import get_matching_data

st.set_page_config(page_title="Opportunity Finder", layout="wide")

st.title("🎯 Opportunity Finder")
st.info("By cross-referencing categories and genres, we identify co-occurrence patterns. " \
"Pairs located in the bottom-right indicate genres that are popular individually but rarely combined. " \
"We call these 'Blue Oceans'. " \
"They represent potential niches where competition is low but market interest is high, signaling promising opportunities for new game development.")

tab1, tab2= st.tabs(["Category Matching", "Genre Matching"])

# --- TAB 1: CATEGORIES ---
with tab1:
    st.header("🔗 Category Synergy")
    cat_df = get_matching_data('categories')
    fig_cat = px.scatter(
        cat_df[cat_df['Games_With_Both'] > 5], # Filter noise
        x="Total_Games_Either",
        y="Games_With_Both",
        size="Synergy_Score",
        color="Synergy_Score",
        color_continuous_scale="RdYlGn",
        hover_name="Pair",
        labels={"Total_Games_Either": "Market Size (A or B)", "Games_With_Both": "Co-occurrence (A and B)"},
        title="Category Co-occurrence Chart"
    )
    st.plotly_chart(fig_cat, use_container_width=True)

# --- TAB 2: GENRES ---
with tab2:
    st.header("🎭 Genre Synergy")
    gen_df = get_matching_data('genres')
    fig_gen = px.scatter(
        gen_df[gen_df['Games_With_Both'] > 5],
        x="Total_Games_Either",
        y="Games_With_Both",
        size="Synergy_Score",
        color="Synergy_Score",
        color_continuous_scale="RdYlGn",
        hover_name="Pair",
        labels={"Total_Games_Either": "Market Size (A or B)", "Games_With_Both": "Co-occurrence (A and B)"},
        title="Genre Co-occurrence Chart"
    )
    st.plotly_chart(fig_gen, use_container_width=True)
