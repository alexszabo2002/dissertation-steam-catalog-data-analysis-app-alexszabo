import streamlit as st
import plotly.express as px
from utils.reviews_analysis import get_sentiment_data

st.set_page_config(page_title="Review Score Analysis", layout="wide")

st.title("⚖️ Review Score & Quality Analysis")

df = get_sentiment_data()

# --- TOP PAGE FILTERS ---
st.markdown("### 🛠️ Global Filters")
c1, c2 = st.columns(2)
with c1:
    all_genres = set()
    df['genres'].str.split(', ').dropna().apply(lambda x: all_genres.update(x))
    selected_genre = st.selectbox("Filter by Genre:", ["All"] + sorted(list(all_genres)))

with c2:
    # Filter for relevant tags only as requested
    relevant_tags = ["Overwhelmingly Positive", "Very Positive", "Mostly Positive", "Positive", "Mixed",
                      "Negative", "Mostly Negative", "Very Negative", "Overwhelmingly Negative"]
    selected_tags = st.multiselect("Review Descriptions (for Correlation Plot):", 
                                   options=df['review_score_description'].unique().tolist(),
                                   default=relevant_tags)

# Applying Filters
if selected_genre != "All":
    df = df[df['genres'].str.contains(selected_genre, na=False)]

# --- COLUMN RANKINGS ---
st.divider()
st.header("🏆 The Leaders Ranked")
st.info("We segment 'Quality' into two tiers: Market Leaders (high-volume success) and Hidden Gems (high-satisfaction niche titles). This prevents popularity bias from obscuring high-quality indie games.")
col1, col2, col3 = st.columns(3)

# 1. Market Leaders (High volume, high score)
with col1:
    st.subheader("🌟 Market Leaders")
    leaders = df[df['steamspy_total_reviews'] >= 50000].sort_values('positive_ratio', ascending=False).head(25)
    fig1 = px.bar(leaders, x='positive_ratio', y='name', hover_data=['name', 'steamspy_total_reviews','positive_ratio'],
                   orientation='h', color='positive_ratio', color_continuous_scale='Greens', range_x=[0,100])
    fig1.update_layout(showlegend=False, yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig1, use_container_width=True)
    st.dataframe(leaders[['name', 'final_price']], use_container_width=True)

# 2. Hidden Gems (Low volume, high score)
with col2:
    st.subheader("💎 Hidden Gems")
    gems = df[(df['steamspy_total_reviews'] < 10000) & (df['steamspy_total_reviews'] > 500)].sort_values('positive_ratio', ascending=False).head(25)
    fig2 = px.bar(gems, x='positive_ratio', y='name', hover_data=['name', 'steamspy_total_reviews','positive_ratio'],
                   orientation='h', color='positive_ratio', color_continuous_scale='Purples', range_x=[0,100])
    fig2.update_layout(showlegend=False, yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig2, use_container_width=True)
    st.dataframe(gems[['name', 'final_price']], use_container_width=True)

# 3. Worst Rated
with col3:
    st.subheader("⚠️ Worst Rated")
    worst = df[df['steamspy_total_reviews'] > 500].sort_values('positive_ratio', ascending=True).head(25)
    fig3 = px.bar(worst, x='positive_ratio', y='name', hover_data=['name', 'steamspy_total_reviews','positive_ratio'],
                   orientation='h', color='positive_ratio', color_continuous_scale='Reds', range_x=[0,100])
    fig3.update_layout(showlegend=False, yaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig3, use_container_width=True)
    st.dataframe(worst[['name', 'final_price']], use_container_width=True)

# --- IMPROVED CORRELATION PLOT ---
st.divider()
st.header("💰 Price vs. Review Score Distribution")
st.info("This plot visualizes the relationship between game prices and their review scores, helping to identify pricing strategies and market trends.")
# Filter by selected tags
plot_df = df[df['review_score_description'].isin(selected_tags)]
plot_df = plot_df[plot_df['price_numeric'] <= 100]

fig_corr = px.scatter(
    plot_df,
    x="price_numeric",
    y="positive_ratio",
    color="review_score_description",
    hover_name="name",
    opacity=0.4,  # Reduces clutter
    marginal_x="histogram", # Shows price density
    marginal_y="violin",    # Shows score density
    trendline="ols",
    template="plotly_dark",
    title="Review Score Density vs Price",
    subtitle="Adding Marginal Distributions for Price (histogram on the top) and Review Score (violin on the right)."
)

st.plotly_chart(fig_corr, use_container_width=True)
