import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from utils.market_analysis import get_market_overview_data, get_top_developers, generate_wordcloud, get_genre_counts

st.set_page_config(page_title="Market Overview", layout="wide")

st.title("🌐 Market Overview")
st.info("Exploration of the most common genres and themes across the Steam Catalog.")

# Load Data
df = get_market_overview_data()

if df.empty:
    st.warning("No data found. Please run the extractor first.")
else:
    # --- SECTION 1: Genre Bubble Chart ---
    st.header("🫧 Genre Frequency")
    st.info("By mapping the frequency of genres, we can identify 'Red Oceans' (highly saturated markets) versus niche genres that may offer untapped opportunities for growth.")
    genre_data = get_genre_counts(df)

    # We use a scatter plot with 'size' to create the bubble effect
    fig_bubble = px.scatter(
        genre_data,
        x="Genre",
        y="Count",
        size="Count",
        color="Genre",
        hover_name="Genre",
        size_max=60,
        title="Distribution of Genres (Bubble Size = Frequency)"
    )
    
    # Clean up the X-axis look
    fig_bubble.update_layout(xaxis_tickangle=-45)
    
    st.plotly_chart(fig_bubble, use_container_width=True)

    # Optional: Show raw counts in an expander
    with st.expander("View Raw Genre Counts"):
        st.dataframe(genre_data, use_container_width=True)

    st.divider()

    # --- SECTION 2: Top Influential Developers ---
    st.header("🏢 Industry Titans")
    st.info("This analysis reveals market concentration. Top 10 developers by volume of titles released in this dataset.")

    # Ensure 'developers' column was included in your get_market_overview_data() SQL query
    dev_data = get_top_developers(df)

    fig_dev = px.bar(
        dev_data,
        x="Games_Count",
        y="Developer",
        orientation='h',
        color="Games_Count",
        color_continuous_scale="Blues",
        text="Games_Count",
        labels={"Games_Count": "Number of Games", "Developer": "Studio Name"}
    )

    # Improve layout for readability
    fig_dev.update_layout(
        yaxis={'categoryorder':'total ascending'}, 
        showlegend=False,
        height=500
    )

    st.plotly_chart(fig_dev, use_container_width=True)

    st.divider()

    # --- SECTION 3: Game Title Wordcloud ---
    st.header("🔠 Title Trends")
    st.info("This visualization identifies the most common linguistic trends in game naming. It highlights the semantic 'hooks' developers use to capture user attention in a crowded marketplace.")
    
    # Unpack the image and the count list
    wc, word_counts = generate_wordcloud(df['name'])
    
    # Matplotlib is needed to display the WordCloud object in Streamlit
    fig_wc, ax_wc = plt.subplots(figsize=(10, 5))
    ax_wc.imshow(wc, interpolation='bilinear')
    ax_wc.axis("off")
    # Make background transparent to match app theme
    fig_wc.patch.set_alpha(0)
    
    st.pyplot(fig_wc)

    # Raw Word Counts Expander
    with st.expander("View Raw Word Frequencies in Titles"):
    # Convert list of tuples to DataFrame
        words_df = pd.DataFrame(word_counts, columns=['Word', 'Frequency'])
        st.dataframe(words_df, use_container_width=True)
