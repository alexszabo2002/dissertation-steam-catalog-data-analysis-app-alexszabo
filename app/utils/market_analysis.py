import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import plotly.express as px
import sqlite3
from collections import Counter
import re

DB_PATH = "data/steam_catalog.db"

def get_market_overview_data():
    conn = sqlite3.connect(DB_PATH)
    # We only need name and genres for these two charts
    df = pd.read_sql_query("SELECT name, genres, developers FROM game_details", conn)
    conn.close()
    return df

def get_top_developers(df, limit=10):
    # Defining the developers we want to exclude from the count (common words that aren't really developers)
    exclude_list = ["Inc.", "Ltd.", "LTD.", "LLC"]

    # Steam developers are often comma-separated: "Dev A, Dev B"
    # We split them and 'explode' to count each individually
    devs_expanded = df['developers'].str.split(', ').explode()
    
    # Clean the strings (remove extra whitespace)
    devs_expanded = devs_expanded.str.strip()
    
    # Remove the excluded names
    # We use ~ (not) and .isin() to filter them out
    filtered_devs = devs_expanded[~devs_expanded.isin(exclude_list)]
    
    # Count and return the top results
    dev_counts = filtered_devs.value_counts().reset_index()
    dev_counts.columns = ['Developer', 'Games_Count']
    
    return dev_counts.head(limit)

def generate_wordcloud(titles_series):
    # Combine all titles into one long string
    text = " ".join(titles_series.dropna().astype(str))
    # Set stopwords
    custom_stopwords = set(STOPWORDS)
    custom_stopwords.update({"the", "and", "or", "i", "ii", "iii", "iv", "v", "x", "s"})
    # Create the wordcloud object
    wc = WordCloud(
        width=800, 
        height=400, 
        background_color='rgba(14,17,24,0)', # Transparent background
        colormap='Blues',
        max_words=50,
        stopwords=custom_stopwords,
        collocations=False
    ).generate(text)
    # Extract exactly what WordCloud counted
    # process_text returns a dict of {word: raw_count} after applying its own filters
    word_counts_dict = wc.process_text(text)
    # Sort them by frequency and take top 50
    sorted_counts = sorted(word_counts_dict.items(), key=lambda x: x[1], reverse=True)[:50]
    return wc, sorted_counts

def get_genre_counts(df):
    # Split the comma-separated genres and explode them into individual rows
    genres_expanded = df['genres'].str.split(', ').explode()
    counts = genres_expanded.value_counts().reset_index()
    counts.columns = ['Genre', 'Count']
    return counts
