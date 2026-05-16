import streamlit as st
import plotly.express as px
from utils.trend_analysis import get_trend_data

st.set_page_config(page_title="Evolution & Trends", layout="wide")

st.title("📈 Evolution & Market Trends")
st.info("Analyzing how game modes and monetization strategies have shifted since 2005. That's the period when steam allowed indie developers to publish directly, leading to a surge in game releases and diversity.")

df = get_trend_data()

if df.empty:
    st.warning("Data not available.")
else:
    # --- GLOBAL FILTERS ---
    st.markdown("### 🛠️ Global Filters")
    c1, c2 = st.columns(2)
    
    with c1:
        all_genres = set()
        df['genres'].str.split(', ').dropna().apply(lambda x: all_genres.update(x))
        selected_genre = st.selectbox("Genre Filter:", ["All"] + sorted(list(all_genres)))

    with c2:
        all_cats = set()
        # Extract categories but EXCLUDE the player-count tags
        df['categories'].str.split(',').dropna().apply(lambda x: all_cats.update([i.strip() for i in x]))
        excluded = {"Multi-player", "Single-player", "Online Multi-Player", "Shared/Split Screen"}
        filtered_cat_list = sorted(list(all_cats - excluded))
        selected_cat = st.selectbox("Additional Category Filter:", ["All"] + filtered_cat_list)

    # Apply Filters
    filtered_df = df.copy()
    if selected_genre != "All":
        filtered_df = filtered_df[filtered_df['genres'].str.contains(selected_genre, na=False)]
    if selected_cat != "All":
        filtered_df = filtered_df[filtered_df['categories'].str.contains(selected_cat, na=False)]

    st.divider()

    # --- CHART 1: Single-player vs Multi-player ---
    st.header("🎮 Player Mode Evolution")
    st.info("A longitudinal look at the shift between single-player and multi-player experiences.")
    
    # Group by year and count occurrences
    mode_trends = filtered_df.groupby('release_year').agg({
        'is_singleplayer': 'sum',
        'is_multiplayer': 'sum'
    }).reset_index()

    # Melt the data for Plotly (Long format)
    mode_melted = mode_trends.melt(id_vars='release_year', var_name='Mode', value_name='Count')
    mode_melted['Mode'] = mode_melted['Mode'].replace({'is_singleplayer': 'Single-player', 'is_multiplayer': 'Multi-player'})

    fig_mode = px.area(mode_melted, x="release_year", y="Count", color="Mode", 
                       title="Volume of Single-player vs Multi-player Releases",
                       color_discrete_map={"Single-player": "#66c0f4", "Multi-player": "#ff4b4b"},
                       line_group="Mode")
    st.plotly_chart(fig_mode, use_container_width=True)

    # --- CHART 2: Free vs Paid ---
    st.header("💰 Monetization Shift")
    st.info("Tracking the evolution of monetization strategies in the gaming industry, a comparison of the rise of free-to-play models against traditional paid games.")
    pay_trends = filtered_df.groupby(['release_year', 'is_free']).size().reset_index(name='Count')
    pay_trends['Type'] = pay_trends['is_free'].map({1: 'Free-to-Play', 0: 'Paid'})

    fig_pay = px.line(pay_trends, x="release_year", y="Count", color="Type", 
                      title="Rise of Free-to-Play vs Paid Games",
                      markers=True,
                      color_discrete_map={"Free-to-Play": "#17ea94", "Paid": "#ff4b4b"})
    st.plotly_chart(fig_pay, use_container_width=True)
