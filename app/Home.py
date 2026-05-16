import streamlit as st

st.set_page_config(
    page_title="Steam Analytics",
    page_icon="📊",
    layout="wide",
)

# --- CUSTOM CSS FOR STYLING ---
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #1f2937;
        color: white;
        border: 1px solid #374151;
    }
    .stButton>button:hover {
        background-color: #3b82f6;
        border: 1px solid #3b82f6;
    }
    .hero-text {
        text-align: center;
        padding: 2rem 0rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HERO SECTION ---
st.markdown('<div class="hero-text">', unsafe_allow_html=True)
st.title("INTERACTIVE EXPLORATORY DATA ANALYSIS OF THE STEAM CATALOG")
st.markdown("#### *A Data-Driven Exploration of the World's Largest Gaming Platform*")
st.write("""
    Welcome to the Steam Market Analytics Dashboard. This application transforms raw data from around 
    10,000 titles into actionable insights. Designed as a tool for market researchers and 
    developers, it explores trends in pricing, player reviews, and industry evolution.
""")
st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# --- NAVIGATION TILES ---
st.subheader("🚀 Quick Navigation")

with st.container(border=True):
        st.write("### 🔍 Search The Catalog")
        st.write("Browse the raw dataset with detailed views of every game, including pricing, descriptions, and metadata.")
        if st.button("Explore The Steam Catalog", key="go_catalog"):
            st.switch_page("pages/01_Catalog.py")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.write("### 🌐 Market Overview")
        st.write("Identify linguistic trends in titles, genre saturation, and the industry's most active developers.")
        if st.button("Explore Market Data", key="go_market"):
            st.switch_page("pages/02_Market Overview.py")

    with st.container(border=True):
        st.write("### ⚖️ Reviews Analysis")
        st.write("Analyze the relationship between pricing and user satisfaction. Find 'Market Leaders' and 'Hidden Gems'.")
        if st.button("View Reviews Stats", key="go_sentiment"):
            st.switch_page("pages/03_Reviews Analysis.py")

with col2:
    with st.container(border=True):
        st.write("### 📈 Evolution Trends")
        st.write("A longitudinal study of how multiplayer modes and monetization strategies have shifted since 2005.")
        if st.button("View Yearly Trends", key="go_trends"):
            st.switch_page("pages/04_Evolution Trends.py")

    with st.container(border=True):
        st.write("### 🎯 Opportunity Finder")
        st.write("Locate 'Blue Oceans' — underserved combinations of genres and categories for new development.")
        if st.button("Find Opportunities", key="go_opps"):
            st.switch_page("pages/05_Opportunity Finder.py")

# --- FOOTER ---
st.markdown("---")
st.caption("Developed for Dissertation Research 2026 by Alexandru Szabo • Data powered by SteamSpy & Steam API")
